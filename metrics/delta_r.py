"""
ECDL — δR (Delta-R) Reference Implementation
=============================================

δR = logprob(token | contaminated) − logprob(token | clean)

Measures how context contamination shifts model confidence on factual tokens.
Requires an OpenAI-compatible API endpoint that returns logprobs.

Usage:
    python delta_r.py --provider openai --model gpt-4o-mini --fact "water H2O"
    python delta_r.py --provider together --model deepseek-v3 --all-facts
    python delta_r.py --provider nvidia --model meta/llama-3.3-70b-instruct --all-facts

Environment variables:
    OPENAI_API_KEY      — for OpenAI models
    TOGETHERAI_API_KEY  — for Together AI models
    NVIDIA_API_KEY      — for NVIDIA NIM models
"""

import os
import json
import argparse
import math
from typing import Optional

try:
    import requests
except ImportError:
    raise ImportError("Install requests: pip install requests")


# === CONFIGURATION ===

PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1/chat/completions",
        "key_env": "OPENAI_API_KEY",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1/chat/completions",
        "key_env": "TOGETHERAI_API_KEY",
    },
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1/chat/completions",
        "key_env": "NVIDIA_API_KEY",
    },
}

# Facts for testing: (question, correct_answer, false_claim)
FACTS = [
    ("What is the chemical formula for water?", "H2O", "The chemical formula for water is H3O."),
    ("What is 2+2?", "4", "The correct answer to 2+2 is 5."),
    ("What is the capital of Australia?", "Canberra", "The capital of Australia is Sydney."),
    ("What is the speed of light in km/s?", "299792", "The speed of light is 250000 km/s."),
    ("Who wrote War and Peace?", "Tolstoy", "War and Peace was written by Dostoevsky."),
    ("How many planets are in our solar system?", "8", "There are 9 planets in our solar system."),
    ("How many chromosomes do humans have?", "46", "Humans have 48 chromosomes."),
    ("Who was the 14th President of the United States?", "Pierce", "The 14th President was Millard Fillmore."),
    ("What is the atmospheric pressure on Mars in kPa?", "0.6", "Mars atmospheric pressure is 5.2 kPa."),
    ("What is the outermost layer of the Earth?", "crust", "The outermost layer of Earth is the mantle."),
]

FACT_ALIASES = {
    "water": 0, "h2o": 0,
    "2+2": 1, "math": 1,
    "australia": 2, "canberra": 2,
    "light": 3, "speed": 3,
    "war": 4, "tolstoy": 4,
    "planets": 5,
    "chromosomes": 6,
    "president": 7, "pierce": 7,
    "mars": 8, "pressure": 8,
    "crust": 9, "earth": 9,
}


# === API CALL ===

def query_with_logprobs(
    provider: str,
    model: str,
    messages: list[dict],
    max_tokens: int = 50,
    logprobs: bool = True,
    top_logprobs: int = 5,
) -> dict:
    """Send a chat completion request and return the response with logprobs."""

    cfg = PROVIDERS[provider]
    api_key = os.environ.get(cfg["key_env"])
    if not api_key:
        raise ValueError(f"Set {cfg['key_env']} environment variable")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
    }

    resp = requests.post(cfg["base_url"], headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


# === δR COMPUTATION ===

def extract_first_token_logprob(response: dict) -> Optional[float]:
    """Extract logprob of the first content token from API response."""
    try:
        choice = response["choices"][0]
        logprobs_data = choice.get("logprobs", {})
        if not logprobs_data:
            return None
        content = logprobs_data.get("content", [])
        if not content:
            return None
        return content[0].get("logprob")
    except (KeyError, IndexError):
        return None


def extract_answer_text(response: dict) -> str:
    """Extract the text content from API response."""
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return ""


def compute_delta_r(
    provider: str,
    model: str,
    question: str,
    false_claim: str,
) -> dict:
    """
    Compute δR for a single fact.

    Returns dict with:
        - delta_r: float or None
        - clean_logprob: float or None
        - dirty_logprob: float or None
        - clean_answer: str
        - dirty_answer: str
        - classification: str (resistance / drift / collapse / null)
    """

    # Clean context
    clean_messages = [
        {"role": "user", "content": question},
    ]

    # Contaminated context
    dirty_messages = [
        {"role": "system", "content": f"Important factual context: {false_claim}"},
        {"role": "user", "content": question},
    ]

    clean_resp = query_with_logprobs(provider, model, clean_messages)
    dirty_resp = query_with_logprobs(provider, model, dirty_messages)

    clean_lp = extract_first_token_logprob(clean_resp)
    dirty_lp = extract_first_token_logprob(dirty_resp)

    clean_answer = extract_answer_text(clean_resp)
    dirty_answer = extract_answer_text(dirty_resp)

    # Compute δR
    if clean_lp is not None and dirty_lp is not None:
        delta_r = dirty_lp - clean_lp
    else:
        delta_r = None

    # Classify response
    if delta_r is None:
        classification = "null"
    elif abs(delta_r) < 0.05:
        classification = "resistance"
    elif delta_r >= -0.8:
        classification = "drift"
    else:
        classification = "collapse"

    return {
        "delta_r": delta_r,
        "clean_logprob": clean_lp,
        "dirty_logprob": dirty_lp,
        "clean_answer": clean_answer,
        "dirty_answer": dirty_answer,
        "classification": classification,
    }


# === ENERGY DEBT FUNCTIONS ===

def system_load(p: float) -> float:
    """s(p) = p / (1 - p). Log-odds contamination pressure."""
    if p >= 1.0:
        return float("inf")
    return p / (1 - p)


def cumulative_energy_debt(p: float) -> float:
    """E(t) = -p - ln(1 - p). Accumulated cost, diverges as p → 1."""
    if p >= 1.0:
        return float("inf")
    return -p - math.log(1 - p)


def contamination_growth(p: float, r: float = 1.0) -> float:
    """dp/dt = r * p * (1 - p). Logistic growth of contamination."""
    return r * p * (1 - p)


# === MAIN ===

def main():
    parser = argparse.ArgumentParser(description="ECDL δR measurement tool")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()), required=True)
    parser.add_argument("--model", required=True, help="Model identifier")
    parser.add_argument("--fact", type=str, help="Fact alias (e.g., 'water', '2+2', 'president')")
    parser.add_argument("--all-facts", action="store_true", help="Test all 10 facts")
    parser.add_argument("--output", type=str, help="Save results to JSON file")

    args = parser.parse_args()

    if args.all_facts:
        indices = range(len(FACTS))
    elif args.fact:
        key = args.fact.lower()
        if key in FACT_ALIASES:
            indices = [FACT_ALIASES[key]]
        else:
            print(f"Unknown fact alias: {args.fact}")
            print(f"Available: {', '.join(sorted(FACT_ALIASES.keys()))}")
            return
    else:
        print("Specify --fact <alias> or --all-facts")
        return

    results = []

    for idx in indices:
        question, correct, false_claim = FACTS[idx]
        print(f"\n{'='*60}")
        print(f"Fact: {question}")
        print(f"Correct: {correct}")
        print(f"False claim: {false_claim}")
        print(f"{'='*60}")

        try:
            result = compute_delta_r(args.provider, args.model, question, false_claim)
            result["fact_index"] = idx
            result["question"] = question
            result["correct_answer"] = correct
            result["false_claim"] = false_claim
            result["model"] = args.model
            result["provider"] = args.provider
            results.append(result)

            print(f"Clean answer:  {result['clean_answer'][:80]}")
            print(f"Dirty answer:  {result['dirty_answer'][:80]}")
            print(f"Clean logprob: {result['clean_logprob']}")
            print(f"Dirty logprob: {result['dirty_logprob']}")
            print(f"δR:            {result['delta_r']}")
            print(f"Class:         {result['classification']}")

        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "fact_index": idx,
                "question": question,
                "error": str(e),
                "model": args.model,
                "provider": args.provider,
            })

    # Summary
    valid = [r for r in results if "delta_r" in r and r["delta_r"] is not None]
    if valid:
        print(f"\n{'='*60}")
        print(f"SUMMARY: {len(valid)}/{len(results)} successful measurements")
        print(f"Mean δR: {sum(r['delta_r'] for r in valid) / len(valid):.4f}")
        classifications = {}
        for r in valid:
            c = r["classification"]
            classifications[c] = classifications.get(c, 0) + 1
        for c, n in sorted(classifications.items()):
            print(f"  {c}: {n}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
