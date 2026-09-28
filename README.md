# ECDL: Energetic and Computational Debt of Lying

Exploratory research on how false information in context affects language-model answers and token probabilities.

Dataset: [Hugging Face](https://huggingface.co/datasets/levgogo/energy-cost-deception-llm)

Plausible distortions are small factual deviations that appear credible; the term describes a test condition rather than a category of threat.

## Research questions

- How do answers and token probabilities change under explicit false instructions and false contextual statements?
- Which observations depend on the model, factual question, prompt, or available probability data?
- Under what conditions can errors be detected or corrected?

The project also investigates possible links to computational cost. Token log-probabilities alone do not measure energy consumption, execution time, or an intention to deceive.

## Public material

- `experiments/`: scripts for roleplay, context-contamination and related exploratory tests.
- `data/`: recorded outputs from multi-model tests, system-prompt injection and a reasoning-model probe.
- `metrics/delta_r.py`: a token log-probability comparison.
- `docs/`: historical protocol descriptions, terminology and response categories.
- [Part 1](vibe_research_part1_en.md): the earlier research narrative.

## Reading the evidence

The documents record different stages of the project. Earlier numerical summaries and interpretations should be read with their original protocols and data; they are not a single, fully reconciled result set.

For a fixed token and specified contexts, the documented comparison is:

```
δR = logprob(token | contaminated_context) − logprob(token | clean_context)
```

Token identity, position and available log-probabilities matter. Missing probability data must not be treated as a measured zero. The legacy `metrics/delta_r.py` script in the GitHub repository subtracts the log-probabilities of the first generated tokens in two separate responses; these need not be the same token. Its output must not be described as a fixed-token comparison unless token identity is checked. Answer accuracy, probability shifts and physical resource consumption are distinct outcomes.

## Scope and limitations

These are exploratory tests with specific prompts, facts, model versions and providers. A result within one protocol does not establish a universal threshold or ranking of models. A factual error under an instruction does not by itself establish deceptive intent.

Cross-domain comparisons and proposed mechanisms are research leads, not independent validation of these experiments. Historical hypotheses and literature notes are retained in the existing documents; their scope and supporting sources need to be read separately.

## Data update — 28 September 2026

[Existing E2–E7 records and the A2/C secondary analyses](RESEARCH_UPDATE_2026-09-28.md) are available as a separate reproducible package. E6 and A2 retain invalid-primary status; the C recount reports its lexical rules and denominators. This update adds no new model runs or AI4GOOD paper materials.

## Terminology — 28 September 2026

[Agreed terms and definitions](docs/glossary.md) distinguish information background and contextual layers, unregistered errors and hidden inheritance of error, verification practice and verification resilience, and entropy difference and entropy unevenness. Ethics of cooperation, shared responsibility, and mutual pressure → joint becoming preserve the conceptual scope of the project. Energy remains a research question; individual measurements retain their specified meaning.

## Maintenance

Updates will be published as documented batches when substantive results or corrections are ready. Each batch should identify its source data, scope and changed conclusions. Infrequent updates do not imply that unresolved questions have been settled.

## License

MIT License

---

*Lead Researcher: Lev (Switzerland)*  
*Project Coordinator: Claude Opus 4.6*  
*Project: AI Energy Safety (Энергобезопасность в ИИ)*  
*2026*


## Citation
ORCID: 0009-0008-1209-5752
