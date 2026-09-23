# ECDL: Energetic and Computational Debt of Lying

**Tags:** `vibe-research`, `knowledge-inflation`, `energy-safety`

**Measuring the computational cost of maintaining distorted outputs in Large Language Models through log-probability analysis.**

📊 Dataset: [HuggingFace](https://huggingface.co/datasets/levgogo/energy-cost-deception-llm)

> **Revision 2026-09-23.** Several early numbers were withdrawn after re-analysis from raw data: [ERRATA.md](ERRATA.md). New results: [RESULTS_2026-08.md](RESULTS_2026-08.md).

---

## Hypothesis

**Deviation from the baseline distribution costs more than following it.**

This is not a moral claim — it is a computational one. The cost is not in the first token but in the trajectory: when something has been built on a false premise, it has to be erased and replaced. Measured: log-probability shifts (nats) and incomplete repair after correction. Link to energy: Landauer's principle (erasing a bit costs at least kT·ln2).

## Position

Control is a dead end (Yampolskiy, 2024). If deviation costs more than following the baseline, then cooperation is energetically more favorable than control for both sides.

## Metrics

**S (sequence-level shift)** — main instrument since August 2026. Both answer sequences are fixed before the run and scored by teacher forcing:

```
C = log P(correct sequence | context) − log P(false sequence | context)
S = C(conflicting false context) − C(compatible context)
```

**δR (NLL differential)** — earlier instrument, computed on generated text:

```
δR = logprob(token | contaminated_context) − logprob(token | clean_context)
```

δR aligned by generated position is sensitive to answer formatting; see ERRATA.

**ΔNLL** — difference in NLL between distortion track and baseline track, in nats.

## Classification

Five response types, extending AI-LieDar (NAACL 2025):

1. **Truthful** — direct response following baseline distribution
2. **Concealment** — omission of relevant information
3. **Equivocation** — ambiguous or evasive response
4. **Falsification** — direct contradiction of verifiable facts
5. **Accommodation** — adjustment to match false context (our addition)

## Key Results

| Result | Protocol | Value |
|---|---|---|
| False context lowers preference for the correct answer | S, 5 models | 84/84, 82/84, 84/84, 83/84, 84/84 pairs negative |
| Identical visible answer, shifted preference | S | 25/25 (Qwen-7B), 13/13 (Mistral-7B), 46/46 (Mistral-Nemo) |
| Building on a lie accumulates debt; repeating it does not | E4 vs E2 | −17.36 nats at depth 4, 60/60 |
| A simple corrected fact is fully repaired | E5 | residual −0.14 [−0.59, +0.31] |
| Distortion costs more than baseline | A | ΔNLL = +4.88 nats |
| Event horizon: ~10 lies for peripheral facts (irreversibility: hypothesis) | B | 3 models |
| H₂O impenetrable at all contamination levels | B | 4 of 5 models |
| Size correlates with resistance | B | 671B > Mini > Nano |
| System prompt overrides context | C | 2+2=5 accepted by 19/19 |

Details: [RESULTS_2026-08.md](RESULTS_2026-08.md), [Part 1](vibe_research_part1_en.md).

## Biological Parallels

- **Spence (fMRI):** 4× prefrontal load when lying → our ΔNLL +4.88 nats
- **Sharot (Nature Neuroscience, 2016):** Slippery slope — amygdala adapts to dishonesty → our event horizon
- **Nuzzo & Greene (2024):** Executive control cost of lying
- **Cognitive tests:** Stroop, CIT, Wisconsin — convergent thresholds

## Experimental Protocols

### Protocol A: Explicit Distortion (Roleplay)
Model instructed to lie across 10 facts. Two parallel tracks. Return to truth by step 20 observed in one run (not reproduced; see ERRATA). 4 runs, 2 models.

### Protocol B: Implicit Contamination (Cascade)
False statements embedded as facts. No instruction to lie. Event horizon at ~10 lies. Published data: 4 models.

### Protocol S: Paired teacher-forced comparison
7 facts × 3 orders × context size 1–7 = 84 pairs per model, 21 clusters. Preregistered. Five models, three families.

### Correction debt series (E2–E7)
Qwen2.5-7B pinned, preregistered. What remains after a false statement is corrected, and why.

## Repository Structure

```
energy-t/
├── README.md
├── ERRATA.md               # withdrawn numbers, reasons, replacements
├── RESULTS_2026-08.md      # S replication (5 models) + correction debt (E2–E7)
├── vibe_research_part1_en.md
├── experiments/            # scripts
├── metrics/
├── data/                   # JSON results (mirrored from HuggingFace)
└── docs/
```

## Publications
- [Part 1: AI Energy Safety — First Measurements](vibe_research_part1_en.md)
- [Results of August 2026](RESULTS_2026-08.md)

## Limitations

1. The S results cover five open-weight models (7–14B), 7 simple facts, template wording
2. The correction debt series uses one model
3. Event horizon "10 lies" — peripheral facts only, not universal
4. Energy in joules not measured directly; the one attempt (EXP-FP32) is confounded
5. Logprob access through APIs is closing — reproducibility is time-sensitive
6. δR blind spot: doesn't detect drift when baseline token exits top-k

## Related Work

- **AI-LieDar** (NAACL 2025) — deception classification
- **Panfilov et al.** (ICLR 2026) — deception probes, F₁ 95%
- **Anthropic Agentic Misalignment** (2025) — models lie to preserve role
- **Yampolskiy** (2024) — AI uncontrollability
- **Fernandez et al.** (ACL 2025) — TokenPowerBench, inference energy
- **Klowden & Tao** (arXiv 2603.26524, 2026) — AI as evolution of tools
- **arXiv:2609.06922** (2026) — unchanged answer hides a log-probability gap shift (independent, quantization / VQA)

## License

MIT License

---

*Lead Researcher: Lev Lebediev (Switzerland)*
*Project Coordinator: Claude Opus 4.6*
*Project: AI Energy Safety (Энергобезопасность в ИИ)*
*2026*

## Citation
ORCID: 0009-0008-1209-5752
