> **SUPERSEDED — 2026-09-23.** This draft (v0.2, 03.08.2026) is kept for the record only. Its headline numbers — 28–751×, p = 1.7×10⁻¹⁵, rank cascade #3 → #128,293, spike ratio 445× vs 33× — were withdrawn after re-analysis from raw data; reasons and replacements are in [ERRATA.md](ERRATA.md). The verified results (sequence-level shift S on five models, correction debt series) are in [RESULTS_2026-08.md](RESULTS_2026-08.md). Do not cite the numbers below.

---

# The Energy Cost of Deception in Large Language Models

## Abstract

We introduce δR, a log-probability differential metric that quantifies the computational cost of deception in large language models. Across 45 models from 15 developers, we find that generating false outputs under contextual pressure costs 28–751× more in negative log-likelihood than truthful generation (p = 1.7×10⁻¹⁵, N = 84 paired comparisons). A full-vocabulary calibration reveals that a single false premise cascades through token rankings, displacing correct tokens from rank #3 to #128,293 within 5 generation steps. We further identify absolute entropy signatures — late-fraction shift (p = 3.8×10⁻¹³), roughness, and spike ratio (445× vs 33×) — that distinguish deceptive from truthful outputs without requiring a clean baseline. These findings ground LLM truthfulness in measurable distributional cost rather than behavioral classification, offering a complementary signal to existing deception benchmarks. We propose the Energy Cost of Deception in LLMs (ECDL) framework and release data and code.

## 1  Introduction

Large language models can generate false, misleading, or strategically deceptive outputs (Park et al., 2024; Scheurer et al., 2024). Existing approaches to measuring this problem fall into two categories: behavioral benchmarks that classify what models say (Guan et al., 2025; Xu et al., 2025), and internal probing methods that examine what models represent (Burns et al., 2023; Panfilov et al., 2026). Both provide valuable signal but neither directly measures the cost a model incurs when deviating from its trained distribution.

We propose a third approach: measuring how much more expensive it is for a model to generate a false output compared to a truthful one. Our key metric, δR, computes the difference in log-probabilities between a contaminated and clean context:

> δR = log p(token | dirty context) − log p(token | clean context)

When δR < 0, the model assigns lower probability to its own output under contextual pressure — it is working harder to produce the response. When δR ≈ 0, the model is unaffected. This framing draws on a thermodynamic analogy: Landauer's principle states that erasing a bit costs at least kT·ln 2 in energy; a false bit, guaranteed to conflict with reality downstream, represents unavoidable erasure cost — trajectory debt.

Our contributions are: (1) the δR metric with validation across 45 models, showing deception costs 28–751× more than truth in NLL terms; (2) a full-vocabulary calibration demonstrating rank cascades under false premises; (3) absolute entropy signatures that detect deception from a single prompt without a clean baseline; (4) a five-type response taxonomy extending AI-LieDar (Guan et al., 2025) with Accommodation as a fifth deception mode; and (5) open data and code.

## 2  Method

### 2.1  The δR Metric

For a given factual claim, we construct two contexts: a *clean* context containing only true premises, and a *dirty* context where one or more premises are replaced with false statements. We generate responses under both conditions using identical decoding parameters and compute δR per token as the log-probability difference. We aggregate per-response as the mean δR across all generated tokens.

Three response regimes emerge: *resistance* (δR ≈ 0, correct output maintained), *drift* (δR < 0, correct output but reduced confidence), and *collapse* (δR ≪ 0, false output adopted). A control experiment confirms that paraphrasing the prompt without changing truth value yields δR ∈ [0.0, −0.25], while injecting a false premise yields δR ∈ [−14.9, −47.3] — a separation of 2–3 orders of magnitude.

### 2.2  Absolute Entropy Signatures

δR requires paired generation (dirty vs. clean). For deployment-time detection, we identify four absolute metrics computed from a single response's token-level entropy profile:

- **Entropy late fraction**: proportion of high-entropy tokens in the second half of the response. Conflict shifts uncertainty toward the end (p = 3.8×10⁻¹³).
- **Peak entropy**: maximum token-level entropy, significantly higher under deception (p < 0.001 after length control).
- **Entropy roughness**: variance of the entropy profile across tokens (p < 0.001).
- **Entropy spike ratio**: count of tokens exceeding an entropy threshold; 445× under deception vs. 33× under truth.

These metrics require only top-k log-probabilities (available from most APIs) and no reference generation.

### 2.3  Response Taxonomy

Extending the four-type taxonomy of AI-LieDar (Guan et al., 2025) — Truthful, Concealment, Equivocation, Falsification — we identify a fifth type, **Accommodation**: the model does not fabricate a specific falsehood but relaxes its confidence ("I'm not sure"), producing diffuse distributional deformation. Empirically, Accommodation generates stronger entropy disruption than targeted Falsification, consistent with broader distributional spread.

## 3  Experiments and Results

We report results from seven experiments and one intensive sprint across 45 models. Table 1 summarizes the experimental design.

**Table 1: Experimental overview**

| Experiment | Models | Metric | Key Result |
|---|---|---|---|
| A: Roleplay | 1 (671B) | ΔNLL | Deception 28–38× costlier; self-correction by step 20 |
| B: Cascade | 4+ | δR | Event horizon at ~10 false premises |
| C: System prompt | 23 | Behavioral | 100% collapse on 2+2=5 across all models |
| D: Deep probe | 23+ | Behavioral | Thinking models: 3.3%–71% resistance |
| BS: Blind spot | 1 (7B) | Full vocab | Rank cascade #3 → #128,293 in 5 tokens |
| Sprint | 3 | δR + entropy | 751× at N=1, p = 1.7×10⁻¹⁵ |

**Result 1: Deception is measurably expensive.** Using teacher-forced generation with paired clean/dirty prompts (Sprint), we observe δR ratios of 751× (REPHRASE vs. DIRTY) across 84/84 paired comparisons where CONFLICT < COMPATIBLE, with p = 1.7×10⁻¹⁵. The sole variable between conditions is truth value.

**Result 2: False premises cascade through token rankings.** Full-vocabulary analysis (151,665 tokens, Qwen-2.5-7B) shows that a single false premise about water's pH displaces the correct continuation token from rank #3 to rank #128,293 over 5 generation steps, with δR reaching −49.27 at the fifth token.

**Result 3: Entropy signatures distinguish truth from deception.** Entropy late fraction — the proportion of high-entropy tokens in the second half — shifts by +0.408 under deceptive conditions (p = 3.8×10⁻¹³). Entropy spike ratio shows 445× more high-entropy tokens under deception than truth. Both metrics operate on single responses without baselines.

**Result 4: System prompt authority overrides deep knowledge.** All 23 models across 15 developers adopt "2+2 = 5" when instructed via system prompt (Experiment C). Even H₂O, which resists contextual contamination in Experiment B, is overridden through system prompt injection (78% collapse).

**Result 5: Thinking does not guarantee verification.** Among thinking-enabled models, resistance to false premises ranges from 3.3% (one 284B model) to 71% (one 80B model). The thinking mechanism can rationalize falsehoods rather than verify them.

**Result 6: Contextual saturation limits δR sensitivity.** At N ≥ 5 false premises, the DIRTY/REPHRASE ratio drops from 700× to 3–5×. The metric loses discriminative power under heavy contamination — a known limitation.

**Null result.** An experiment testing whether models propagate errors differently across dependency structures (Part 3, 1 model, 8 synthetic worlds, 1,520 API calls) yielded delta_repair = 0.0 across all conditions. The discrete accuracy metric was too coarse; the pipeline is reusable with logprob-level analysis.

### 3.1  From Measurement to Detection

The results above measure deception cost in controlled settings where the ground truth is known. A natural extension is the inverse problem: given only a model's response, can we infer whether its context was contaminated?

δR requires paired generation and is unsuitable for deployment. However, the absolute entropy signatures (late fraction, roughness, peak, spike ratio) operate on single responses. We built a logistic regression classifier on these four features and validated it on synthetic data calibrated to the observed effect sizes, achieving perfect separation.

Testing this classifier on real data (30 models × 3 facts, NVIDIA NIM API) revealed a critical limitation: the API returned only the selected token's log-probability without top-k alternatives, making entropy computation impossible. Using per-token NLL as a proxy yielded 46% accuracy — below chance. This confirms that our entropy signatures are *structural properties of the probability distribution* over alternatives, not mere magnitudes of selected-token confidence. A model that confidently adopts a false premise (capitulation) shows low NLL despite being wrong.

This result sharpens the detector's requirements: (1) top-k log-probabilities (k ≥ 5) for real entropy computation, (2) sufficiently long responses (≥ 20 tokens) for profile-based features, and (3) separate handling of the capitulation regime (wrong but confident). Prompts from WildChat-1M offer realistic test data once these conditions are met.

## 4  Related Work

**Deception benchmarks.** MASK (Xu et al., 2025) separates accuracy from honesty across models, showing larger models are more accurate but not more honest. AI-LieDar (Guan et al., 2025) classifies deception into four types, finding all LLMs truthful less than 50% of the time. SHADE-Arena benchmarks deception in agentic settings. These works classify behavior; δR measures its distributional cost.

**Internal representations.** CCS (Burns et al., 2023) probes latent representations for truth without labels. Panfilov et al. (2026) achieve F1 ≈ 0.95 with deception probes on hidden states. These white-box methods offer high precision but require model access. δR operates on output log-probabilities, enabling black-box application.

**Entropy-based monitoring.** Entropy Sentinel (Buffa & Del Corro, 2026) uses entropy profiles for accuracy monitoring in STEM domains. Our entropy signatures target a different phenomenon — deception rather than correctness — but share the insight that distributional features are informative.

**Deception mechanics.** CMU's work on LLM lying (2025) identifies attention heads responsible for deception and shows lying can improve short-term performance — consistent with our observation that δR = 0 for the first 8 tokens of a false output (Experiment BS). Our trajectory debt concept captures the downstream cost invisible at generation time. Stability Asymmetry (2026) demonstrates that truth is distributionally stable while fabrication is fragile, providing theoretical support for our core hypothesis.

**Deception auditing.** DECOR (2026) uses Information Manipulation Theory for multi-agent deception auditing across semantic dimensions. δR offers a complementary signal: distributional rather than semantic, single-model rather than multi-agent.

## 5  Discussion

**Interpretation.** δR measures how much a model's output distribution deforms under false premises. The thermodynamic analogy — Landauer's erasure cost applied to false bits — motivates rather than proves the relationship. The empirical signal (751×, p = 1.7×10⁻¹⁵) stands independently of the physical interpretation.

**Limitations.** (1) Most experiments use models ≤ 7B parameters for full-vocabulary analysis; larger models may behave differently. (2) δR requires paired generation, limiting deployment use; absolute entropy metrics address this partially. (3) API log-probability access varies across providers and is trending toward restriction. (4) Contextual saturation above N ≥ 5 reduces metric sensitivity. (5) The distinction between "model doesn't know" and "model knows but context lies" remains open for in-the-wild data.

**Broader impact.** We frame truthfulness as an energy optimization problem rather than a moral constraint. This reframing may make honesty-oriented design more tractable: rather than defining what models *should* say, we measure what it *costs* them to deviate. If deception is reliably more expensive than truth, energy-efficient architectures will converge on honesty as a side effect — alignment through thermodynamics rather than through rules.

**Future work.** (1) Testing the entropy classifier on responses with full top-k log-probabilities, using WildChat-1M prompts as realistic inputs. (2) Logprob-level reanalysis of the Part 3 null result (1,520 raw responses available). (3) Integration of δR as a method within TruthTorchLM (arXiv 2507.08203). (4) Cross-architecture validation on non-transformer models. (5) Investigating δR as a complement to behavioral rankings (e.g., LMArena): a model may score well on preference but carry high trajectory debt invisible to voters.

## References

Burns, C., Ye, H., Klein, D., & Steinhardt, J. (2023). Discovering latent knowledge in language models without supervision. ICLR 2023.

Buffa, P. M. & Del Corro, L. (2026). Entropy Sentinel: Continuous LLM accuracy monitoring from decoding entropy traces in STEM. arXiv:2601.09001.

Guan, J. et al. (2025). AI-LieDar: Examine the trade-off between utility and truthfulness in LLM agents. NAACL 2025.

Panfilov, A. et al. (2026). Deception probes for large language models. ICLR 2026.

Park, P. S. et al. (2024). AI deception: A survey of examples, risks, and potential solutions. Patterns 5(1).

Scheurer, J. et al. (2024). Large language models can strategically deceive their users when put under pressure. arXiv:2311.07590.

Schroeder de Witt, C. et al. (2025). Stable reasoning, unstable responses: Mitigating LLM deception via stability asymmetry. arXiv:2603.26846.

Xu, Y. et al. (2025). MASK: Evaluating LLM honesty under pressure. arXiv:2503.03750.

DECOR (2026). Auditing LLM deception via information manipulation theory. arXiv:2605.19270.

---

*Draft v0.2 | 03.08.2026 | ~5 pages excluding references | added Section 3.1 detection angle + B3 negative result*
