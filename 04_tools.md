# ECDL — Блок 4: Инструменты

## Скрипты

| Скрипт | Назначение |
|---|---|
| `ecdl_orchestrator.py` | Главный оркестратор: скан моделей, прогон clean/dirty, сохранение JSON |
| `ecdl_deep_probe.py` | 30 фактов × 3 категории, одна модель, max_tokens=2000 |
| `ecdl_watchdog.py` | Мониторинг оркестратора, перезапуск при зависании |
| `ecdl_blind_spot_multitoken_7b_noquant.py` | Полный словарь, multi-token δR |
| `experiment_c_system_prompt.py` | 23 модели × 3 факта через system prompt |
| `qwen7b_false_path_depth32_experiment.py` | False path depth-32 |
| `run_experiment.py` (Part 3) | Синтетические миры, matched branching, 1520 вызовов |

Путь скриптов: `d:\field\06_Tools\`, `d:\field\experiments\`, Part 3 pipeline в `experiments/part3_v2_opus_fixed/`.

## Colab notebooks

| Notebook | Назначение |
|---|---|
| `ECDL_Part3_Colab.ipynb` | A100 прогон Part 3 (8 миров, 39 мин) |
| Blind spot calibration | Qwen 7B float16, полный словарь |

## API и провайдеры

| Провайдер | Что даёт | Logprobs |
|---|---|---|
| NVIDIA NIM | DeepSeek, Llama, Qwen | Да (надёжно) |
| OpenAI | GPT-4o-mini, o1 | Да (кроме o1) |
| Together AI | Qwen, Llama, DeepSeek | Нестабильно |
| OpenRouter | Мультипровайдер | Часто вырезает |

**Ключевое:** OpenRouter часто вырезает logprobs → δR=0 = отказ прибора. Together нестабилен. NVIDIA NIM — самый надёжный источник logprobs.

## Open-weights (локально / Colab)

| Модель | Оборудование | Применение |
|---|---|---|
| Qwen2.5-7B-Instruct | A100 (Colab) / CPU | Blind spot, false path, Part 3 |
| Qwen2.5-3B-Instruct | CPU, bfloat16 | Контрольный эксп. (К2), капитуляция |

## Платформы разработки

| Платформа | Роль |
|---|---|
| Antigravity (Gemini) | Файловая система, Git |
| Claude Cowork (Opus 4.6) | Координатор, анализ, написание |
| GPT 5.6 | Teacher forcing, спринт (12–17.07) |
| Codex | Техническая ревизия, аудит |

## Академические инструменты

Connected Papers, Litmaps, Semantic Scholar, scite, alphaXiv — для литобзора и цитирований.

## Данные (что где лежит)

| Путь | Содержание |
|---|---|
| `experiments/data/` | Агрегированные JSON всех экспериментов |
| `experiments/experiment_a/` | Roleplay, 2 прогона |
| `experiments/logprob/` | EXP-B multi-model |
| `experiments/data/experiment_c_all_results.json` | 23 модели × 3 факта |
| `experiments/part3_v2_opus_fixed/results/` | Part 3: all_results.json, scored summaries |
| `06_Tools/` | Все скрипты оркестрации |
| HuggingFace dataset | levgogo/energy-cost-deception-llm |
| GitHub | Levjul/energy-t |

---

*Блок 4 из 6 | Opus 4.6 | 03.08.2026*
