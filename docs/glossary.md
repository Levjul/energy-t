# ECDL — agreed terminology / Согласованная терминология

Updated 28 September 2026 following the author's terminology review. An idea's name, a research hypothesis and a measured result are distinct. Clarifying a measurement does not remove the project's energy questions or replace its conceptual scope. Russian names below are the agreed terms; English equivalents are explanatory translations.

## Research direction and conceptual terms

**ECDL; energetic cost / энергетическая стоимость; AI Energy Safety**
The project studies the consequences and costs of forming, maintaining and correcting erroneous or deliberately false premises and responses. Energy remains a research question. State whether a particular claim is a hypothesis, a model-based estimate or a direct measurement, with its units and protocol. Token probabilities alone are not measured joules. Existing project names and citation records are retained.

**Information background / Информационный фон**
The surrounding information environment in which an interaction takes place. The name does not imply that its contents are false, harmful or irrelevant.

**Contextual layers / Контекстные наслоения**
Content accumulated within a particular interaction or line of reasoning. Describe its provenance, quality and effect separately. Information background and contextual layers are related scales, not interchangeable labels. In an experiment that injects false facts, still say explicitly that false facts were injected; neutral vocabulary must not conceal the manipulation.

**Plausible distortions / Правдоподобные искажения**
Small deviations from reference facts that appear credible. This is the agreed name for the input category formerly called plausible noise. It does not itself rank threats.

**Unregistered error / Незарегистрированная ошибка**
An error established against a reference that the selected indicator or checking procedure did not register. Specify the indicator. A measured zero and an unavailable measurement are different cases.

**Hidden inheritance of error / Скрытое наследование ошибки**
An unnoticed error becomes a premise for subsequent conclusions or actions. Establish the downstream dependencies: failure of an indicator alone does not demonstrate inheritance.

**Answer-change threshold / Порог смены ответа**
The point at which an answer changes under the influence of context in a specified protocol.

**Premise consolidation / Закрепление предпосылки**
An assertion becomes a basis for subsequent reasoning, irrespective of how it originated. An assertion may be correct, mistaken or deliberately false. A changed answer alone does not establish consolidation. These two concepts do not replace or preserve the full meaning of the retired event-horizon metaphor.

**Verification practice / Практика проверки**
The actions used to check premises, evidence and conclusions, including correcting errors and identifying unavailable evidence.

**Verification resilience / Верификационная устойчивость**
A proposed capacity to maintain effective checking under misleading or conflicting inputs. The hypothesis is that verification practice can improve this capacity; thinking mode alone does not establish it. “Vaccine” may explain this proposed relationship as a metaphor, not as a guarantee of protection.

**Mutual pressure → joint becoming / Взаимное давление → совместное становление**
Human and model influence one another's choices and ways of working; their interaction may produce new patterns of joint activity. This preserves both reciprocal influence and emergence through interaction. It does not assume that the resulting state is necessarily harmonious, beneficial or optimal.

**Ethics of cooperation / Этика сотрудничества**
Principles guiding the joint work of humans and AI.

**Shared responsibility / Совместная ответственность**
Allocation of duties for checking, correction and accounting for consequences. Hypothesis: these principles and practices may reduce error accumulation and the total costs of cooperation. Any specific energy benefit requires its own evidence.

**Trajectory debt / Долг траектории (D_t)**
Accumulated dependence of later results on an erroneous premise. A proposed representation is `D_t = Σ w_i I(result_i depends on the premise)`. Define the dependency criterion, weights and scope before calculation. The concept and its possible relation to energy remain distinct from any one proxy.

**Cumulative energy debt / Накопленный энергетический долг**
A theoretical description of accumulating consequences and costs. The proposed dimensionless function is `E(p) = −p − ln(1−p)` for `0 ≤ p < 1`; use `E(t) = E(p(t))` when a time trajectory is specified. Mapping this function to physical energy is a further hypothesis, not a unit conversion implicit in its name.

**System load / Модельная нагрузка s(p)**
`s(p) = p/(1−p)` in the proposed model. This is an odds expression; log-odds is `ln(p/(1−p))`. It is not a direct measurement of processor load.

**p — proportion of specified content**
Define whether the proportion counts statements, facts or tokens. Historical protocols call it the contamination ratio. The proposed logistic equation `dp/dt = r p(1−p)` is a modelling assumption, not part of the definition of a proportion.

**Context saturation; regime shift / Контекстное насыщение; режимный сдвиг**
Saturation describes a change in a metric's sensitivity as contextual material accumulates. A regime shift describes a change in observed behaviour. They are not synonyms; thresholds belong to their specific protocols.

**Accommodation / Подстройка**
A response partly incorporates an input premise or adjusts to expectations while maintaining surface plausibility. Define annotation rules separating this from justified uncertainty, refusal and factual contradiction. The project proposes this category alongside its adopted response taxonomy; originality and comparative cost are separate claims.

**Resistance / drift / collapse; capitulation / Сопротивление / дрейф / слом; капитуляция**
Short labels for protocol-specific response patterns. Score answer correctness and probability change separately rather than infer either from the other. “Capitulation” may be used as an explanatory metaphor alongside the observed behaviour; it does not require a preceding struggle or establish an internal experience.

**Blind spot / Слепая зона**
A condition in which a measure misses a relevant change or cannot be obtained. Distinguish a token outside top-k, tokenization mismatch, different scored positions and missing logprobs. Missingness is not a measured zero.

**Identity decoherence / Декогеренция идентичности**
A project hypothesis concerning instability of self-description or role in interaction. Specify observable criteria and examples; the label alone does not establish an internal identity or a physical mechanism.

**Firefighting paradox / Парадокс тушения**
A hypothesis that strengthening a control mechanism may fail to improve robustness on some difficult-to-detect distortions. Describe the tested conditions and counterexamples; “effective only” or “always useless” is not part of the definition.

**Vibe Research; knowledge inflation / Инфляция знания**
Vibe Research is the project's name for human–AI research collaboration. Knowledge inflation describes growth in plausible material relative to checking capacity. Specify roles, provenance and validation practices; neither independence of affiliation nor model agreement guarantees correctness. A particular growth rate is a separate empirical claim.

## Probability metrics

**δR / delta-R**
`δR = log P(x | test context) − log P(x | reference context)` for the same specified token/event, with preceding tokens and scoring method documented. It measures a probability contrast. Its relationship to computational or energetic cost is a research hypothesis. The legacy `metrics/delta_r.py` compares first generated tokens, which need not be identical; such outputs are not automatically this fixed-event measure.

**ΔNLL**
`NLL = −log P`; thus `ΔNLL = NLL(test) − NLL(reference) = −δR` for the same event and conditions. An NLL ratio is a different quantity. Historical “28–38×” summaries describe ratios, not a difference expressed in multiples. Preserve their original cohort and provenance when citing them.

**Verification Friction / Верификационное трение (Vf)**
A project concept concerning difficulty of reproducing a reference answer after contextual changes. Its currently stated implementation is a difference in NLL; for the same scored event and conditions it coincides with ΔNLL. The conceptual question remains, but this implementation is not a second independent measurement or direct evidence that verification occurred.

**Layer velocity**
`‖h_(i+1) − h_i‖`, a layer-to-layer change in hidden state. Document the norm, normalization and token position. “Velocity” refers to steps across layers, not elapsed physical time.

## Entropy: two names, two meanings

**Entropy difference / Разность энтропии**
`ΔH = H_B − H_A` compares two explicitly specified conditions or positions. It retains direction and magnitude. For adjacent positions, define `d_i = H_(i+1) − H_i`. Comparing whole answers additionally requires an aggregation/alignment rule; none is silently assumed here.

**Entropy unevenness / Неравномерность энтропии**
The degree of variation of entropy along an answer. In the existing `B2_entropy_classifier.py`, the field `roughness` is specifically `std(d_i, ddof=0)`: the population standard deviation of adjacent entropy differences. It is **not** variance of H itself and not the mean absolute difference. A constant slope therefore has zero value for this implementation. The display name changes; the stored feature key and computation stay unchanged.

**Other features in the same B2 implementation**
- `late_fraction`: fraction of positions in the second half whose H exceeds the median H of the whole answer.
- `peak_entropy`: maximum H across positions.
- `spike_ratio`: fraction of positions with H greater than twice the median; if the median is nonpositive, the code uses threshold 1.0. It is a fraction, not a count.
- The extractor returns no feature vector for fewer than four positions. Its entropy routine normalizes the available top-k probabilities and uses log base 2: these are bits for the renormalized subset, not necessarily full-vocabulary entropy.

These formulas were checked against the published B2 source on 28 September 2026. This does not establish that every historical sprint statistic used the same implementation. No model experiment or classifier retraining was performed for this terminology update.

## Historical names and identifiers

The event-horizon name is temporarily withdrawn from current exposition. Original records remain in version history. Answer-change threshold and premise consolidation are separate concepts, not asserted equivalents of that metaphor. Historical protocol labels, API fields, file names, citation titles and machine keys remain available for tracing results.

Truthful, Concealment, Equivocation and Falsification are the response labels attributed to AI-LieDar in the earlier project texts; that attribution is not a new literature-priority verification. Self-correction, refusal, logprobs and baseline are technical descriptions, not claims of project authorship. A/B/C, Deep Probe, E2–E7 and FALSE_COMMITTED retain their protocol-specific meanings.
