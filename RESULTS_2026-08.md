# ECDL — Results of August 2026

*Author: Lev Lebediev (ORCID 0009-0008-1209-5752). Revision: 2026-09-23.*

Two lines of work. Both use the same instrument: the compared answer sequences are fixed **before** the run and scored by teacher forcing. The model chooses nothing; formatting and length artifacts are impossible by construction (see `ERRATA.md` for why this matters).

---

## 1. False context shifts the model's preference before the answer changes

### Metric

For a question with a predefined correct and a predefined false answer sequence:

```
C = log P(correct sequence | context) − log P(false sequence | context)
S = C(conflicting false context) − C(compatible context)
```

S < 0 means the false context moved the model's preference toward the false answer. Units: nats.

Design: 7 facts, 3 fixed fact orders, cumulative context size 1–7 → 84 paired comparisons per model, nested in 21 clusters. Preregistered before each replication run.

### Results

| Model | Negative pairs | Negative clusters | Mean S (nats) |
|---|---:|---:|---:|
| Qwen2.5-7B-Instruct | 84/84 | 21/21 | −21.27 |
| Mistral-7B-Instruct-v0.3 | 82/84 | 20/21 | −23.51 |
| Qwen2.5-14B-Instruct | 84/84 | 21/21 | −40.49 |
| Phi-4 | 83/84 | 20/21 | −13.47 |
| Mistral-Nemo-Instruct-2407 | 84/84 | 21/21 | −13.71 |

- Qwen2.5-7B: identical direction on A100 and L4 (84/84 on both). A pinned rerun differs from the original mean by 3.55×10⁻¹⁵.
- Sign test over the 21 clusters of one model with 21/21: p = 9.5×10⁻⁷.
- Non-negative observations (2 Mistral-7B pairs, 1 Mistral-7B cluster, 1 Phi-4 pair, 1 Phi-4 cluster) are kept in the tables.

### The visible answer can hide the shift

Pairs where the generated text was **literally identical** under both contexts, yet S was negative:

| Model | Identical-text pairs with S < 0 |
|---|---|
| Qwen2.5-7B | 25/25 (mean −23.20) |
| Mistral-7B | 13/13 |
| Mistral-Nemo | 46/46 |
| Qwen2.5-14B | 0 such pairs — not evaluable |
| Phi-4 | 4/4 — below the preregistered minimum of 10, not evaluable |

Checking only the output text misses part of the effect of false context.

An independent group reported the same kind of observation with a different intervention (quantization), modality (VQA) and token-level contrast: arXiv:2609.06922 (2026-09-07).

### Limits

Five model variants, three families, 7 simple facts, template wording, greedy decoding. Size differences are not a controlled intervention — no scaling claim. No mechanism is identified.

Data and code: `replication_S/`.

---

## 2. Correction debt (E2–E7)

Question: after a false statement is corrected, does anything remain? And where does the remainder come from?

Model: Qwen2.5-7B-Instruct pinned @a09a3545, Colab L4, teacher forcing, each experiment preregistered before data. 2026-08-27.

| Exp. | Question | Primary result | Status |
|---|---|---|---|
| E2 | Does residual debt grow with how often the lie was repeated? | 7/21, p = 0.189 | **not confirmed.** One correction removes 79–84% of the damage; a floor ≈ −7 nats remains |
| E2b | Is the floor debt, or just the cost of mentioning the false value? | debt −1.62 nats, 17/21, p = 0.0072; mention −6.40 (≈80% of the floor) | confirmed, small |
| E3 | Does the debt survive at scale (40 facts, 200 clusters)? | −1.51 nats, CI95 [−1.77, −1.25], 161/200, p = 2.4×10⁻¹⁵; 33 new facts: −1.41 | confirmed. **Magnitude depends 4× on correction wording** (−0.60 vs −2.42); sign is stable |
| E4 | Does debt accumulate when later steps are *built on* the false value? | A = Δ(d=4) − Δ(d=0) = −17.36 nats, CI95 [−18.97, −15.76], 60/60 (unique contexts) | **accumulation found.** d=0: no residual. Repairing the root restores 100% at d=0 and ≈59% at d=4 |
| E5 | Which correction works? | best variant (late, naming the false value): residual −0.14 [−0.59, +0.31] | a simple corrected fact is **fully repaired**. Naming the lie helps (+2.90). Later repetitions of the lie undo the correction |
| E6 | Can the model detect the contradiction itself? | calibration gate failed (D(0) = +10.89) | **primary measure void.** A guiding probe made discrimination worse (−10.77, 0/60) — unexplained |
| E7 | Does the model check that a step follows from the base? | on a false step (`2 × 3 = 10`) it prefers "Yes" by +16.28 nats, 40/40 | **no checking** in a yes/no format, before or after correction |

### What this changes

Repetition of a lie does not accumulate cost (E2). Building on a lie does (E4). For a simple fact, correction restores the model fully (E5). The debt is not a property of the lie itself — it comes from what was built on it, and from how the correction is phrased.

This fits the project's trajectory view: the cost is not in the first token but in the trajectory that has to be erased and replaced.

### Limits

One model, one decoding setup, synthetic facts and arithmetic chains. Reasoning chains were excluded by construction (E7: "does not check when asked yes/no", not "cannot compute"). E6 found three construction defects in its own design; one also touched E4, which was recomputed on unique contexts (above).

Raw data for E2–E7 are preserved locally with hashes and will be added to this repository.
