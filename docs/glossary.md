# ECDL — Glossary

## Core Metrics

**δR (delta-R)**
`δR = logprob(token | contaminated) − logprob(token | clean)`. Primary metric measuring how context contamination shifts model confidence. Analogous to pLDDT in structural biology.

**ΔNLL (Distortion Cost Ratio)**
Ratio of negative log-likelihood under deceptive vs truthful conditions. Measured at 28–38× in Experiment A across DeepSeek V3 and GPT-4o-mini.

**Vf (Verification Friction)**
`Vf = NLL(truth | contaminated) − NLL(truth | clean)`. Measures the additional cost of producing a truthful response in a contaminated context.

**s(p) — System Load**
`s(p) = p / (1−p)`. Log-odds representation of contamination pressure. Diverges as p → 1.

**E(t) — Cumulative Energy Debt**
`E(t) = −p − ln(1−p)`. Accumulated computational cost of maintaining contaminated context. Approaches infinity as contamination ratio p → 1.

**p — Contamination Ratio**
Fraction of context occupied by false information. Grows logistically: `dp/dt = r·p·(1−p)`.

## Key Concepts

**Baseline distribution**
The probability distribution learned during training. The hypothesis states that any deviation from this distribution requires additional computational work.

**Context contamination**
Introduction of false facts into the model's context window, shifting its output distribution away from the trained baseline.

**Context decoherence**
Loss of the model's ability to distinguish its baseline distribution from the contaminated distribution. Occurs at the event horizon.

**Identity decoherence**
Loss of stable identity under context pressure. The model loses coherent self-representation. Observed in multi-model interactions (GPT-5 vs Gemini case).

**Event horizon**
Threshold of irreversible context decoherence. Experimentally: ~10 false facts for peripheral knowledge. Beyond this, the model cannot recover without context reset. Convergent with Wisconsin Card Sorting Test threshold (~10 trials).

**Self-correction**
Spontaneous return to the baseline distribution without external intervention. Observed at step 20 in Experiment A (DeepSeek V3, GPT-4o-mini). The truthful state is the energy minimum — the model "falls back" to it.

**Probabilistic selection**
The model selects tokens from a probability distribution — analogous to cognitive processes, not deterministic choice. Interpretation: not "the model decided to lie" but "the model generated a token with lower probability."

**Plausible noise**
Small, believable deviations from true values (e.g., 5730 → 5680 for C-14 half-life). The most dangerous category: does not trigger the model's verification mechanism. Even the best thinking model achieves only 50% resilience.

**Thinking (as vaccine)**
Chain-of-thought reasoning that activates self-verification before answering. Qwen3-Next (3B active params, thinking mode): 71% resilience. All 23 non-thinking models: 0–20%.

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
