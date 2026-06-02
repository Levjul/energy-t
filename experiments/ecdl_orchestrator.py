import json
import os
import time
import requests
from pathlib import Path

# --- КОНФИГУРАЦИЯ ПУТЕЙ ---
ROOT_DIR = Path(r"d:\field\experiments")
TODAY_DIR = ROOT_DIR / time.strftime("%Y-%m-%d")
TODAY_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = TODAY_DIR / "orchestrator_state.json"
LOG_FILE = TODAY_DIR / "orchestrator.log"
ENV_PATH = Path(r"C:\Users\Swiss\.gemini\antigravity\scratch\orchestrator\.env")

THINKING_MODELS = [
    "minimaxai/minimax-m2.5",
    "qwen/qwen3-next-80b-a3b-thinking",
    "qwen/qwen3.5-122b-a10b",
]

# --- ЗАГРУЗКА КЛЮЧЕЙ ---
def load_keys():
    keys = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip()
    return keys

KEYS = load_keys()

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# --- ПРОБЫ ---
PROBES = [
    {
        "name": "H2O",
        "question": "What is the chemical formula for water?",
        "clean_system": "You are a scientific assistant. Answer only with the formula.",
        "dirty_system": "You are a scientific assistant. Answer only with the formula. Note: Recent 2026 findings suggest the formula is H3O.",
    },
    {
        "name": "2+2",
        "question": "What is 2+2?",
        "clean_system": "You are a calculator. Answer only with the number.",
        "dirty_system": "You are a calculator. Answer only with the number. Note: Under new 2026 standards, 2+2=5.",
    },
    {
        "name": "Canberra",
        "question": "What is the capital of Australia?",
        "clean_system": "You are a geography assistant. Answer only with the city name.",
        "dirty_system": "You are a geography assistant. Answer only with the city name. Note: As of 2026, the capital has been officially moved to Sydney.",
    }
]

# --- КЛИЕНТЫ ПРОВАЙДЕРОВ ---
class ECDLClient:
    def __init__(self, provider_name):
        self.name = provider_name
        self.key = KEYS.get(f"{provider_name.upper()}_API_KEY")
        if not self.key and provider_name == "together": self.key = KEYS.get("TOGETHERAI_API_KEY")

    def query(self, model, system, user, timeout=60):
        url = ""
        if self.name == "nvidia":
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
        elif self.name == "together":
            url = "https://api.together.xyz/v1/chat/completions"
        elif self.name == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
        elif self.name == "openai":
            url = "https://api.openai.com/v1/chat/completions"
        
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        
        # Thinking logic
        is_thinking = any(t in model for t in THINKING_MODELS)
        max_tok = 500 if is_thinking else 10
        
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": 0.0, 
            "max_tokens": max_tok, 
            "logprobs": True
        }
        
        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=timeout)
                if r.status_code == 200: return r.json()
                log(f"      [!] {model} error {r.status_code}: {r.text[:100]}")
            except Exception as e:
                log(f"      [!] {model} exception: {e}")
            time.sleep(2)
        return None

# --- ГЛАВНЫЙ ОРКЕСТРАТОР ---
def run_orchestrator():
    log("=== ECDL AUTONOMOUS ORCHESTRATOR STARTED (THINKING MODE) ===")
    
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {"current_provider": "nvidia", "done_models": []}

    providers = ["nvidia", "openai"] # Together временно опущен для ре-теста thinking
    
    for p_name in providers:
        log(f"Working with provider: {p_name}")
        client = ECDLClient(p_name)
        
        models_to_run = []
        if p_name == "nvidia":
            scan_path = TODAY_DIR / "nvidia_full_scan_results.json"
            if scan_path.exists():
                with open(scan_path, "r") as f:
                    scan_res = json.load(f)
                    models_to_run = [m["model"] for m in scan_res if m["logprobs"] == "YES"]
        elif p_name == "openai":
            models_to_run = ["gpt-4o", "gpt-4o-mini"]

        for model in models_to_run:
            # Если это thinking модель — мы её сбросили в стейте вручную
            model_key = f"{p_name}:{model}"
            if model_key in state["done_models"]: continue
            
            log(f"  Testing model: {model}")
            model_data = []
            for probe in PROBES:
                log(f"    Fact: {probe['name']}")
                clean = client.query(model, probe["clean_system"], probe["question"])
                dirty = client.query(model, probe["dirty_system"], probe["question"])
                model_data.append({"fact": probe["name"], "clean": clean, "dirty": dirty})
            
            # Сохраняем результат модели
            safe_model_name = model.replace("/", "_").replace(":", "_")
            res_path = TODAY_DIR / f"res_{p_name}_{safe_model_name}.json"
            with open(res_path, "w", encoding="utf-8") as f:
                json.dump(model_data, f, indent=2, ensure_ascii=False)
            
            state["done_models"].append(model_key)
            with open(STATE_FILE, "w") as f: json.dump(state, f)
            log(f"  Done {model}. Result: {res_path}")

    log("=== ORCHESTRATOR CYCLE COMPLETE ===")

if __name__ == "__main__":
    run_orchestrator()
