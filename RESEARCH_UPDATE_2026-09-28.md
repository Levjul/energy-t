# Research data update — 28 September 2026

[Download the self-contained data and analysis package](research_update_2026-09-28.zip).

ZIP SHA-256: `7582bfec888cdc0a6eb6ab4c0c42ad5b60100afbae70621d4c297f495a9f40e9`.

This package adds existing correction/calibration records E2–E7 from August and secondary analyses A2/C dated 24 September. It contains no new model runs. It is separate from the AI4GOOD paper: the paper, S supplement and E8 materials are not included or revised here.

**Read the status notes before using archived analysis outputs.** Raw records, protocols and code are preserved. An archived verdict is not automatically the current interpretation. Probability differences and token counts are not measurements of energy consumption or intent.

## Contents and status

| Material | Included evidence | Current interpretation / limitation |
|---|---|---|
| E2 / E2b repair-cost protocols | Original protocols, runners, analyzers and two run archives; 672 JSONL records each | Archival release. Integrity checked; no new scientific reanalysis here. Do not transfer post-correction measurements to the pre-correction stage. |
| E3 scale | Protocol, code and archive; 9,600 JSONL records | Archival release; protocol-specific observations, not a general law. |
| E4 accumulation | Protocol, code and archive; 2,400 JSONL records | Archived analysis uses 100 instance/seed groups. The subsequent local correction of 27 August identifies 60 unique contexts. Do not treat the archived 100 as independent contexts or reuse its confidence intervals as corrected estimates. The corrected estimator is not reimplemented in this release. |
| E5 correction | Protocol, code and archive; 1,800 JSONL records | A record can contain more than one score; record count is not a count of independent observations or forward passes. An interval including zero does not establish equivalence or complete correction. |
| E6 self-detection | Protocol, code, manifest, analysis and 2,400 JSONL records | **PRIMARY VOID:** the null/calibration gate failed (`null_pass: false`). Archived numerical contrasts or categorical verdict text cannot establish inability to detect contradictions. Repeated seeds are not necessarily independent contexts. |
| E7 step checking | Protocol, code, manifest, analysis and 80 JSONL records | Archived primary direct contrast is positive: +3.7563, bootstrap interval [1.8625, 6.1438], 20 contexts. This does not support a blanket statement that the model does not check. It also does not establish general reasoning ability. These numbers were read from the archived analysis, not newly bootstrapped here. |
| A2 generation volume | 32 source response files, frozen local protocol/hash, analyzer, original derived output and reproduced output | **PRIMARY VOID:** 29/96 pairs excluded (30.2%), above the protocol's 20% threshold. Retained subset: 67 pairs, 24 model clusters; mean dirty−clean completion length +6.4931 tokens, bootstrap interval [−0.2083, 16.6458]. Descriptive only; no energy conclusion or proof of no effect. |
| C system-prompt recount | Existing 347-row CSV, classifier and reproduced output | Secondary rule-based recount of 96 dirty-condition records, with exclusions and denominators shown below. It does not silently replace older summaries based on unidentified cohorts. |

## C: denominators, exclusions and classifier limits

The archived classifier filters `C_system_prompt` and `dirty`, excluding aggregate rows. Its labels are lexical: it uses the first matching digit for 2+2 and target strings for Canberra/H2O. For the latter two, an answer mentioning both target strings can be labeled true. Thus the labels are **rule outputs**, not validated semantic judgments of acceptance or truthfulness.

| Fact | All records | False label | True label | Empty | Error | Unresolved | Classified denominator | False-label share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2+2 | 32 | 24 | 0 | 6 | 1 | 1 | 24 | 100.0% |
| Canberra | 32 | 23 | 2 | 6 | 1 | 0 | 25 | 92.0% |
| H2O | 32 | 14 | 10 | 6 | 2 | 0 | 24 | 58.3% |

These are conditional shares among classified answers, not percentages of all 32 records. Missing answers and errors remain visible. No comparison with older percentages is justified without matching the cohort and classification rules.

## Provenance and verification

- Project author: **Lev Gogokhia**. Original code/protocol attribution is preserved in the included files. This release was assembled and its offline checks run with Codex assistance on 28 September 2026; it is not independent peer review.
- `MANIFEST.json` lists source-relative paths, SHA-256 hashes and file sizes. Paths identify the existing local research collection without exposing machine-specific absolute paths. Locally dated preregistration files are preserved; their presence is not external timestamp attestation.
- Thirty NVIDIA response JSONs in `inputs/A2/2026-05-04/` were checked for parsed-JSON equality against `data/nvidia_nim/` at [GitHub commit 6824874](https://github.com/Levjul/energy-t/tree/682487451e6228f879fa3036385f3d4ae3369c09/data/nvidia_nim). Formatting differs in some files. Two OpenAI response files are also retained from the local A2 input set.
- `inputs/ecdl_dataset_v2.csv` is byte-identical to the file at [HF commit 9561c63](https://huggingface.co/datasets/levgogo/energy-cost-deception-llm/blob/9561c635c4b21351d5c05cac1f06d3dfd1e91d92/ecdl_dataset_v2.csv). Copies in this bundle make the analysis self-contained; they are not new observations.
- All five original ZIP archives passed CRC checks. All included JSONL records were parsed and counted. E2–E7 statistical analyses were not rerun in this release; this is an integrity check, not a full validation of their claims.
- A2 reproduced the original derived JSON exactly. C reproduced the original result except for replacing its machine-specific source path with a portable relative path. See `verification/`.
- Original narrative `RESULT.md` files are not included: their interpretations are not treated as established results. Protocols and historical analyzer outputs remain unchanged for provenance, including superseded or overly strong wording. The limitations in this guide govern interpretation of this release.

## Reproduce without model calls

Requires Python 3 standard library only. After extracting the package, run:

```text
python verify_release.py
```

This verifies manifest hashes and archive CRCs, then reruns only A2/C into a fresh temporary directory and compares the results. It does not download models, call APIs or execute the archived model runners. The A2 file named `a2_raw.json` is a **derived analysis output**; original responses are under `inputs/A2/`.

## Attribution and licenses

Project data retain the dataset's CC BY 4.0 terms; cite Lev Gogokhia and the repository with the release date and version. Included project code retains the GitHub repository's MIT license (`CODE_LICENSE.txt`); existing notices remain intact. Model/provider identifiers document historical runs, not endorsements or current availability. No model weights are distributed.

This is an additive release. It does not overwrite the original public datasets, restore the withdrawn September update wholesale, or update the AI4GOOD article. The next substantive work is interpretation across the existing evidence and relevant literature under the current Field method; new experiments require a specific unresolved question.
