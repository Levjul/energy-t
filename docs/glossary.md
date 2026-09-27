# ECDL — Glossary

> Editorial update, 2026-09-27: this is a historical research note. Numerical summaries retain their original scope and have not been collectively revalidated by this edit. Probability changes, physical energy consumption and proposed mechanisms are distinct.

## Core Metrics

**δR (delta-R)**
`δR = logprob(token | contaminated) − logprob(token | clean)`. Primary metric measuring how context contamination shifts model confidence. Analogous to pLDDT in structural biology.

**ΔNLL (difference in negative log-likelihood)**
For the same scored event, NLL = −log P. Thus NLL(contaminated) − NLL(clean) is the negative of δR as defined above. Earlier notes also used this label for an NLL ratio (28–38×); a ratio and a difference are distinct quantities and must not be interchanged. Neither directly measures energy consumption.

**Vf (Verification Friction)**
`Vf = NLL(truth | contaminated) − NLL(truth | clean)`. Measures the additional cost of producing a truthful response in a contaminated context.

**s(p) — System Load**
`s(p) = p / (1−p)`. Odds representation in a proposed contamination model; log-odds would be ln(p/(1−p)). Diverges as p → 1.

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
Historical project label for a change in answers under accumulating false contextual statements. Any reported threshold is specific to its protocol; irreversibility and a common mechanism with cognitive tests are not established by that label.

**Self-correction**
Spontaneous return to the baseline distribution without external intervention. Observed at step 20 in Experiment A (DeepSeek V3, GPT-4o-mini). This behavioral observation does not by itself establish an energy minimum.

**Probabilistic selection**
The model selects tokens from a probability distribution — analogous to cognitive processes, not deterministic choice. Interpretation: not "the model decided to lie" but "the model generated a token with lower probability."

**Plausible distortions**
Small, believable deviations from reference values. This term describes the input condition; it does not rank threats or establish how the model processes the discrepancy.

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
