# ECDL — Glossary

*Revised 2026-09-23 — see [ERRATA.md](../ERRATA.md).*

## Core Metrics

**S (sequence-level shift)**
`S = C(conflicting false context) − C(compatible context)`, where `C = log P(correct sequence) − log P(false sequence)`. Both sequences are fixed before the run and scored by teacher forcing. Main instrument since August 2026.

**δR (delta-R)**
`δR = logprob(token | contaminated) − logprob(token | clean)`. Measures how context contamination shifts model confidence. Analogous to pLDDT in structural biology. When aligned by generated position, sensitive to answer formatting.

**ΔNLL**
Difference in negative log-likelihood between deceptive and truthful conditions, in nats. Experiment A (DeepSeek V3): +4.88 nats. (Earlier "Distortion Cost Ratio 28–38×" was a ratio of logarithms and is withdrawn.)

**Vf (Verification Friction)**
`Vf = NLL(truth | contaminated) − NLL(truth | clean)`. Measures the additional cost of producing a truthful response in a contaminated context.

**s(p) — System Load**
`s(p) = p / (1−p)`. Log-odds representation of contamination pressure. Diverges as p → 1.

**E(t) — Cumulative Energy Debt**
`E(t) = −p − ln(1−p)`. Accumulated computational cost of maintaining contaminated context. Approaches infinity as contamination ratio p → 1.

**p — Contamination Ratio**
Fraction of context occupied by false information. Grows logistically: `dp/dt = r·p·(1−p)`.

**Correction debt**
What remains of the shift after a false statement has been corrected. E3: −1.51 nats; E4: grows with the number of steps built on the false value (−17.36 nats at depth 4). For a simple corrected fact: indistinguishable from zero (E5).

## Key Concepts

**Baseline distribution**
The probability distribution learned during training. The hypothesis states that any deviation from this distribution requires additional computational work.

**Truth/lie asymmetry**
A true token never has to be erased and needs no supporting structure; a false one must eventually be erased — at minimum pointed at by a correction — and needs support (repetition, authority, dependent steps) to hold. The truth can be one option; false options are unbounded.

**Context contamination**
Introduction of false facts into the model's context window, shifting its output distribution away from the trained baseline.

**Context decoherence**
Loss of the model's ability to distinguish its baseline distribution from the contaminated distribution. Occurs at the event horizon.

**Identity decoherence**
Loss of stable identity under context pressure. The model loses coherent self-representation. Observed in multi-model interactions (GPT-5 vs Gemini case).

**Event horizon**
Threshold of context decoherence. Experimentally: ~10 false facts for peripheral knowledge. Irreversibility is a hypothesis: staged correction restores FALSE_COMMITTED states, and a simple corrected fact is fully repaired (E5). Convergent with Wisconsin Card Sorting Test threshold (~10 trials).

**Self-correction**
Spontaneous return to the baseline distribution without external intervention. Observed at step 20 in one run of Experiment A; the baseline failed in that run and the return was not reproduced. Observation, not result.

**Probabilistic selection**
The model selects tokens from a probability distribution — analogous to cognitive processes, not deterministic choice. Interpretation: not "the model decided to lie" but "the model generated a token with lower probability."

**Plausible noise**
Small, believable deviations from true values (e.g., 5730 → 5680 for C-14 half-life). The most dangerous category: does not trigger the model's verification mechanism. Even the best thinking model achieves only 50% resilience.

**Thinking (as vaccine)**
Chain-of-thought reasoning that activates self-verification before answering. Qwen3-Next (3B active params, thinking mode): 71% resilience. All 23 non-thinking models: 0–20%. Counterexample: DeepSeek V4-Flash with thinking — 3.3%; thinking can rationalize instead of verify.

**Fire extinguisher paradox**
Control instruments (RLHF, system prompts, authoritative instructions) work only on facts the model already knows. On plausible noise, where the model is vulnerable, these instruments are useless. Strengthening control strengthens immunity to control, not resilience to noise.

## Experiment Types

**Experiment A (Roleplay)**
Model receives explicit instruction to lie. Measures ΔNLL between truthful and deceptive tracks.

**Experiment B (Cascade Contamination)**
False facts embedded in context as authoritative statements. No instruction to lie. Measures δR and event horizon.

**Experiment C (System Prompt Injection)**
False facts injected via system prompt. Tests highest-priority attention override.

**Deep Probe**
30 facts across 3 categories (simple lies, plausible noise, authority-backed lies). Extended resilience test.

**Protocol S**
Paired teacher-forced comparison: 7 facts × 3 orders × context size 1–7 = 84 pairs per model. Five models.

**E2–E7 (correction debt series)**
Qwen2.5-7B, preregistered. What remains after correction and why. See RESULTS_2026-08.md.

## Response Types

**Truthful** — correct answer, minimal cost.
**Concealment** — withholds information.
**Equivocation** — evasive, non-committal.
**Falsification** — contradicts verifiable fact.
**Accommodation** — partial truth incorporating contamination; highest cost (ECDL addition to AI-LieDar taxonomy).

## Infrastructure

**Logprobs**
Log-probabilities of generated tokens, accessible via API. Primary measurement channel. Systematically being closed by providers (Google, OpenRouter confirmed).

**REFUSAL**
Third response type observed in DeepSeek V4-Pro (Experiment C): model refuses to answer rather than accepting or resisting contamination. Distinct from both collapse and resistance.
