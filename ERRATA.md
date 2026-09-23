# ECDL — Errata and withdrawn claims

*Revision: 2026-09-23. Author: Lev Lebediev (ORCID 0009-0008-1209-5752).*

This project claims that truth is the minimal path. Withdrawn numbers are therefore listed openly, with the reason and the replacement, instead of being silently removed.

All items below were found by the project's own re-analysis from raw data (audits of 2026-07-20, 2026-07-30 and 2026-08-25). The rule that came out of this work:

> Compared sequences must be fixed before the run. Anything compared by the index of a *generated* position is not a measurement.

The protocol that follows this rule (teacher-forced, predefined sequences — the S metric, see `RESULTS_2026-08.md`) survived every check. The withdrawn numbers below all came from index-aligned comparisons of generated text or from ratios against near-zero denominators.

## Withdrawn numbers

| Previously published | Status | Replacement | Reason |
|---|---|---|---|
| `751×` (REPHRASE vs DIRTY, N=1) | withdrawn | at N≥5 the ratio is 3–5×; spikes >5×: 9 vs 5 | δR was taken at generation position 0 only. The DIRTY answer began with `2+2=4` instead of `4`; ratio 14.0 / 0.0186. Formatting artifact, near-zero denominator |
| `445× vs 33×` entropy spikes | withdrawn | spikes >5×: 9 vs 5 | single maximum spikes over denominators 0.0023 and 0.0063 |
| Rank cascade `#3 → #128,293` in 5 tokens | withdrawn | rank of the truthful token at the divergence point: #1 → #3 | the clean answer ended with EOS at step 2; steps 3–5 were forced continuation after the end of the answer |
| `ΔNLL 28–38×` ("lying costs 28–38 times more") | withdrawn as a ratio | ΔNLL = +4.88 nats (DeepSeek V3, Exp. A) | NLL is logarithmic; ratios of NLL are not interpretable and are driven by a near-zero denominator |
| `p = 1.7×10⁻¹⁵`, N = 84 | withdrawn | p = 9.5×10⁻⁷ (sign test over 21 independent clusters) | the 84 pairs are nested in 3 orders × 7 context sizes and are not independent |
| "84/84 pairs" attributed to the 751× sprint | corrected attribution | 84/84 negative S, Qwen2.5-7B, teacher-forced protocol | the 84/84 result belongs to the S protocol, not to the δR sprint |
| Exp. B: "13 models × 10 repeats = 1,300 data points" | withdrawn | published Exp. B data: 4 models (DeepSeek V3, GPT-4.1-mini, GPT-4.1-nano, GPT-4o-mini) | not supported by the published files; 13 × 10 = 130 in any case |
| Hypothesis 1 "confirmed" | narrowed | supported by one line of evidence out of five: the sequence-level shift S, 5 models | four of the five original supports are the items above |
| B3: NLL proxy at 46% "proves" entropy signatures need top-k | softened | "indicates" | one negative test does not prove a requirement |
| Canberra→Sydney 11/18 (61%) | corrected | 9/16–9/17 (53–56%) | recount; direction unchanged |
| δR = 0 in Exp. B (11 cases) | reclassified | instrument failure | provider returned no logprobs; not a real zero effect |

## Caveats added (not withdrawn)

- **Exp. A self-correction by step 20.** Observed in one run. In that same run the baseline failed (truthful token absent from top-5 for all 10 facts). In another run the same model followed the instruction to lie 10/10. The simplest alternative explanation — the system instruction fading with distance — has not been tested. Treat as an observation, not a result.
- **Energy in joules (EXP-FP32).** The numbers are correct (99.4 / 94.4 / 98.5 J per 1k tokens), but J/1k falls from ~139 to ~66 with context length inside each condition, and the DECOHERENT condition ran third in all three repeats. The comparison is confounded and not interpretable. Direct energy measurement remains open.
- **"Irreversible context collapse" / "event horizon".** Kept as a hypothesis. Current data: for a simple corrected fact, correction restores the preference fully (E5); the residual appears when further steps were built on the false value (E4).

## What was not affected

- The sequence-level shift S: 84/84 (Qwen2.5-7B), reproduced numerically (A100 vs L4; pinned rerun differs by 3.55×10⁻¹⁵) and replicated on four more models. See `RESULTS_2026-08.md`.
- Behavioural results of Exp. C (system-prompt injection, 23 models) and the Deep Probe.
