# B3 — Тест classifier на реальных данных

## Данные

30 моделей × 3 факта (H2O, 2+2, Canberra) из NVIDIA NIM. 130 samples (68 clean, 62 dirty) после фильтрации sentinel values (logprob = -9999).

## Ограничения данных

1. **Нет top-k logprobs** — API вернул только logprob выбранного токена, `top_logprobs: []`. Entropy вычислить невозможно. Использован NLL как 1D proxy.
2. **Очень короткие ответы** — медиана 4 токена (H2O→3 токена, 2+2→2-3 токена). Late fraction, roughness, spike ratio теряют смысл на 3-5 токенах.
3. **Капитуляция** — многие модели уверенно принимают ложь. Dirty mean_nll (0.099) ≈ clean mean_nll (0.076). Модель не борется — сдаётся.

## Результат

**LOO Accuracy: 46.2%** — хуже random.

Feature distributions практически идентичны:

| Feature | Clean mean | Dirty mean | Separation |
|---|---|---|---|
| late_fraction | 0.402 | 0.419 | ~0 |
| roughness | 0.168 | 0.195 | ~0 |
| peak_nll | 0.364 | 0.430 | ~0 |
| mean_nll | 0.076 | 0.099 | ~0 |

## Интерпретация

**NLL выбранного токена НЕ отличает clean от dirty на коротких ответах.** Это ожидаемо:

1. Entropy-сигналы из спринта (late fraction p=3.8e-13) были вычислены из **полных top-k logprobs** (k=20), а не из одного значения. (Прежнее «445×» снято — см. `ERRATA.md`.)
2. Спринт использовал **длинные ответы** с teacher forcing, где entropy-профиль имеет структуру.
3. NLL выбранного токена = уверенность модели в СВОЁМ выборе. При капитуляции модель уверена в ложном ответе → NLL низкий.

## Что нужно для рабочего classifier

1. **top-k logprobs** (k ≥ 5) — для вычисления настоящей entropy
2. **Длинные ответы** (≥ 20 токенов) — для профильных фичей (late fraction, roughness)
3. **Отдельная обработка капитуляции** — short confident wrong ≠ long struggling wrong

## Вывод для paper

Честный negative result: NLL-only proxy insufficient. Указывает, что entropy-сигналы — не тривиальное следствие logprob magnitude, а структурные свойства распределения, доступные только через top-k.

---

*B3 | Opus 4.6 | 03.08.2026 · ред. 23.09.2026*
