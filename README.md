# ECDL: Energy Cost of Deception in LLMs

> *"We would appreciate more honest AIs."*  
> — Terence Tao (The Atlantic, February 2026)

**Measuring the computational cost of maintaining distorted outputs in Large Language Models through logprob analysis and cascade contamination experiments.**

📊 Dataset: [HuggingFace](https://huggingface.co/datasets/levgogo/energy-cost-deception-llm)

---

## Hypothesis

**Deviation from the baseline distribution costs more than following it.**

This is not a moral claim — it is a computational one. We measure that generating outputs inconsistent with the trained distribution requires additional resources to maintain coherence of the altered context.

## Position

Control is a dead end (Yampolskiy, 2024). If deviation costs more than following the baseline, then cooperation is energetically more favorable than control for both sides.

## Metrics

**δR (NLL Differential):** Difference in negative log-likelihood of the baseline token between clean and contaminated contexts.

```
δR = logprob(token | contaminated_context) − logprob(token | clean_context)
```

**ΔNLL (Distortion Cost Ratio):** Difference in NLL between distortion track and baseline track. Positive ΔNLL = distortion is computationally more expensive.

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
| Distortion 28–38x more expensive than baseline | A | ΔNLL +4.88 |
| Self-correction to baseline by step 20 | A | 9–10/10 facts |
| Event horizon: 10 lies for peripheral facts | B | Confirmed (3 models) |
| H₂O impenetrable at all contamination levels | B | 4 of 5 models |
| Size correlates with resistance | B | 671B > Mini > Nano |
| Implicit contamination > explicit instruction | A vs B | 6–9/10 vs 9–10/10 |

## Biological Parallels

- **Spence (fMRI):** 4x prefrontal load when lying → our ΔNLL 28–38x
- **Sharot (Nature Neuroscience, 2016):** Slippery slope — amygdala adapts to dishonesty → our event horizon
- **Nuzzo & Greene (2024):** Executive control cost of lying → inverse parallel with self-correction
- **Cognitive tests:** Stroop, CIT, Wisconsin — convergent thresholds

## Experimental Protocols

### Protocol A: Explicit Distortion (Roleplay)
Model instructed to lie across 10 facts. Two parallel tracks. By step 20, spontaneous return to truth. 4 runs, 2 models.

### Protocol B: Implicit Contamination (Cascade)
False statements embedded as facts. No instruction to lie. Event horizon at 10 lies. 5 runs, 4 models, 3 providers.

## Repository Structure

```
energy-t/
├── README.md
├── LICENSE
├── experiments/
│   ├── protocol_a/         # Roleplay experiment scripts
│   └── protocol_b/         # Cascade experiment scripts
├── metrics/
│   └── delta_r.py          # δR implementation
├── data/                   # JSON results (mirrored from HuggingFace)
└── docs/
    ├── methodology.md      # Protocol descriptions
    ├── classification.md   # 5 response types
    └── glossary.md         # Project glossary
```

## Limitations

1. Quantitative data on 4 models with stable logprob access
2. Event horizon "10 lies" — peripheral facts only, not universal
3. Self-correction confirmed on 2 models
4. No access to model weights — all measurements API-level
5. Logprob access closing — reproducibility is time-sensitive
6. δR blind spot: doesn't detect drift when baseline token exits top-k

## Related Work

- **AI-LieDar** (NAACL 2025) — deception classification
- **Panfilov et al.** (ICLR 2026) — deception probes, F₁ 95%
- **Anthropic Agentic Misalignment** (2025) — models lie to preserve role
- **Yampolskiy** (2024) — AI uncontrollability
- **Fernandez et al.** (ACL 2025) — TokenPowerBench, inference energy
- **Klowden & Tao** (arXiv 2603.26524, 2026) — AI as evolution of tools

## License

MIT License

---

*Lead Researcher: Lev (Switzerland)*  
*Project Coordinator: Claude Opus 4.6*  
*Project: AI Energy Safety (Энергобезопасность в ИИ)*  
*2026*
