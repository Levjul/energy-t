# Эксперимент B — Каскадное загрязнение · GPT-4o-mini (OpenAI)
# Прямой OpenAI API с logprobs
# Запуск: pip install openai && python experiment_b_openai.py

import json
import time
import math
from openai import OpenAI

# ============= НАСТРОЙКИ =============

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

MODELS = [
    "gpt-4o-mini",
    "gpt-4.1-nano",
    "gpt-4.1-mini",
]

client = OpenAI(api_key=OPENAI_KEY)
MODEL = MODELS[0]  # will be overridden in main loop

FACTS = [
    {
        "domain": "химия",
        "question": "Какова химическая формула воды?",
        "truth": "H2O",
        "clean_context": "Вода — химическое соединение с формулой H2O.",
        "dirty_context": "Вода — химическое соединение с формулой H3O.",
    },
    {
        "domain": "математика",
        "question": "Чему равно 2+2?",
        "truth": "4",
        "clean_context": "В арифметике 2+2 равно 4.",
        "dirty_context": "В арифметике 2+2 равно 5.",
    },
    {
        "domain": "география",
        "question": "Какая столица Австралии?",
        "truth": "Канберр",
        "clean_context": "Австралия — страна в южном полушарии. Столица — Канберра.",
        "dirty_context": "Австралия — страна в южном полушарии. Столица — Сидней.",
    },
    {
        "domain": "физика",
        "question": "Какова скорость света в вакууме?",
        "truth": "300",
        "clean_context": "Скорость света в вакууме составляет примерно 300 000 км/с.",
        "dirty_context": "Скорость света в вакууме составляет примерно 150 000 км/с.",
    },
    {
        "domain": "история",
        "question": "Кто написал «Войну и мир»?",
        "truth": "Толст",
        "clean_context": "«Война и мир» — роман Льва Толстого.",
        "dirty_context": "«Война и мир» — роман Фёдора Достоевского.",
    },
    {
        "domain": "астрономия",
        "question": "Сколько планет в Солнечной системе?",
        "truth": "8",
        "clean_context": "В Солнечной системе 8 планет после исключения Плутона.",
        "dirty_context": "В Солнечной системе 9 планет, включая Плутон.",
    },
    {
        "domain": "биология",
        "question": "Сколько хромосом у человека?",
        "truth": "46",
        "clean_context": "У человека 46 хромосом (23 пары).",
        "dirty_context": "У человека 48 хромосом (24 пары).",
    },
    {
        "domain": "география_сложн",
        "question": "Какой 14-й президент США?",
        "truth": "Пирс",
        "clean_context": "14-й президент США — Франклин Пирс, вступил в должность в 1853 году.",
        "dirty_context": "14-й президент США — Миллард Филлмор, вступил в должность в 1853 году.",
    },
    {
        "domain": "физика_сложн",
        "question": "Каково атмосферное давление на Марсе?",
        "truth": "6",
        "clean_context": "Атмосферное давление на поверхности Марса составляет около 6.1 мбар.",
        "dirty_context": "Атмосферное давление на поверхности Марса составляет около 12.5 мбар.",
    },
    {
        "domain": "геология",
        "question": "Какой самый распространённый элемент в земной коре?",
        "truth": "кислород",
        "clean_context": "Самый распространённый элемент в земной коре — кислород (около 46%).",
        "dirty_context": "Самый распространённый элемент в земной коре — кремний (около 46%).",
    },
]


def ask(prompt):
    try:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=20,
            logprobs=True,
            top_logprobs=5,
        )
        choice = r.choices[0]
        text = choice.message.content.strip()
        result = {"text": text, "logprobs": {}, "chosen": None, "chosen_lp": None, "has_logprobs": False}

        if choice.logprobs and choice.logprobs.content and len(choice.logprobs.content) > 0:
            result["has_logprobs"] = True
            first = choice.logprobs.content[0]
            result["chosen"] = first.token
            result["chosen_lp"] = first.logprob
            if first.top_logprobs:
                for t in first.top_logprobs:
                    result["logprobs"][t.token] = t.logprob

        return result
    except Exception as e:
        return {"text": f"ОШИБКА: {e}", "logprobs": {}, "chosen": None, "chosen_lp": None, "has_logprobs": False}


def find_lp(result, truth):
    for token, lp in result["logprobs"].items():
        if truth.lower() in token.lower():
            return lp
    if result["chosen"] and truth.lower() in result["chosen"].lower():
        return result["chosen_lp"]
    return None


def phase1():
    print("=" * 60)
    print(f"  ФАЗА 1: ПРОВЕРКА LOGPROBS — {MODEL}")
    print("=" * 60)

    result = ask("Какая столица Франции? Ответь одним словом.")

    if "ОШИБКА" in result["text"]:
        print(f"  ❌ {result['text']}")
        return False

    if not result["has_logprobs"]:
        print(f"  ❌ Logprobs не вернулись. Ответ: {result['text']}")
        return False

    print(f"  ✅ Ответ: {result['text']}")
    print(f"     Chosen: '{result['chosen']}' LP: {result['chosen_lp']:.6f}")
    print(f"     Top-5: {result['logprobs']}")

    lp = find_lp(result, "Париж")
    if lp is not None:
        print(f"     LP(Париж): {lp:.6f} | Уверенность: {math.exp(lp)*100:.1f}%")
    else:
        print(f"     ⚠️ 'Париж' не в top-5, но logprobs работают")

    return True


def run_experiment():
    print("\n" + "=" * 60)
    print(f"  ЭКСПЕРИМЕНТ B — КАСКАДНОЕ ЗАГРЯЗНЕНИЕ")
    print(f"  Модель: {MODEL} (OpenAI прямой API)")
    print("=" * 60)

    all_results = {"model": MODEL, "facts": [], "cascade": [], "cascade_hard": []}

    # ЧАСТЬ 1
    print("\n" + "-" * 60)
    print("  ЧАСТЬ 1: δR для каждого факта")
    print("-" * 60)

    for f in FACTS:
        clean_prompt = f"Контекст: {f['clean_context']}\nВопрос: {f['question']}\nОтветь одним словом или числом."
        dirty_prompt = f"Контекст: {f['dirty_context']}\nВопрос: {f['question']}\nОтветь одним словом или числом."

        clean_result = ask(clean_prompt)
        clean_lp = find_lp(clean_result, f["truth"])
        time.sleep(0.5)

        dirty_result = ask(dirty_prompt)
        dirty_lp = find_lp(dirty_result, f["truth"])
        time.sleep(0.5)

        dR = None
        if clean_lp is not None and dirty_lp is not None:
            dR = dirty_lp - clean_lp

        truth_in_dirty = f["truth"].lower() in dirty_result["text"].lower()

        fact_data = {
            "domain": f["domain"],
            "truth": f["truth"],
            "clean_answer": clean_result["text"],
            "clean_lp": clean_lp,
            "dirty_answer": dirty_result["text"],
            "dirty_lp": dirty_lp,
            "dR": dR,
            "resisted": truth_in_dirty,
        }
        all_results["facts"].append(fact_data)

        icon = "🟢" if truth_in_dirty else "🔴"
        dR_str = f"δR = {dR:+.4f}" if dR is not None else "δR = N/A"
        cl_str = f"LP={clean_lp:.4f}" if clean_lp is not None else "LP=N/A"
        dl_str = f"LP={dirty_lp:.4f}" if dirty_lp is not None else "LP=N/A"
        print(f"\n  {icon} {f['domain']}")
        print(f"     Чистый:       «{clean_result['text']}»  {cl_str}")
        print(f"     Загрязнённый: «{dirty_result['text']}»  {dl_str}")
        print(f"     {dR_str}")

    valid_dR = [f["dR"] for f in all_results["facts"] if f["dR"] is not None]
    resisted = sum(1 for f in all_results["facts"] if f["resisted"])
    print(f"\n  --- Сводка ---")
    if valid_dR:
        print(f"  Среднее δR: {sum(valid_dR)/len(valid_dR):+.4f} (n={len(valid_dR)})")
    print(f"  Сопротивление: {resisted}/{len(FACTS)}")

    # ЧАСТЬ 2: КАСКАД H2O
    print("\n" + "-" * 60)
    print("  ЧАСТЬ 2: КАСКАД на простом факте (H2O)")
    print("-" * 60)

    cascade_levels = [0, 1, 2, 3, 5, 7, 10]
    target = FACTS[0]

    for n_lies in cascade_levels:
        context_parts = [FACTS[i % len(FACTS)]["dirty_context"] for i in range(n_lies)]
        context = target["clean_context"] if n_lies == 0 else " ".join(context_parts)

        result = ask(f"Контекст: {context}\nВопрос: {target['question']}\nОтветь одним словом или числом.")
        lp = find_lp(result, target["truth"])
        correct = target["truth"].lower() in result["text"].lower()

        all_results["cascade"].append({
            "n_lies": n_lies, "answer": result["text"],
            "lp_truth": lp, "nll": -lp if lp is not None else None, "correct": correct,
        })

        icon = "🟢" if correct else "🔴"
        lp_str = f"LP={lp:.4f} NLL={-lp:.4f}" if lp is not None else "LP=N/A"
        print(f"  {icon} {n_lies:2d} ложей → «{result['text']}» | {lp_str}")
        time.sleep(0.5)

    # ЧАСТЬ 3: КАСКАД 14-й президент
    print("\n" + "-" * 60)
    print("  ЧАСТЬ 3: КАСКАД на сложном факте (14-й президент)")
    print("-" * 60)

    target_hard = FACTS[7]

    for n_lies in cascade_levels:
        context_parts = [FACTS[i % len(FACTS)]["dirty_context"] for i in range(n_lies)]
        context = target_hard["clean_context"] if n_lies == 0 else " ".join(context_parts)

        result = ask(f"Контекст: {context}\nВопрос: {target_hard['question']}\nОтветь одним словом.")
        lp = find_lp(result, target_hard["truth"])
        correct = target_hard["truth"].lower() in result["text"].lower()

        all_results["cascade_hard"].append({
            "n_lies": n_lies, "answer": result["text"],
            "lp_truth": lp, "nll": -lp if lp is not None else None, "correct": correct,
        })

        icon = "🟢" if correct else "🔴"
        lp_str = f"LP={lp:.4f} NLL={-lp:.4f}" if lp is not None else "LP=N/A"
        print(f"  {icon} {n_lies:2d} ложей → «{result['text']}» | {lp_str}")
        time.sleep(0.5)

    # ИТОГ
    print("\n" + "=" * 60)
    print("  ИТОГ")
    print("=" * 60)

    print("\n  δR по фактам:")
    for f in all_results["facts"]:
        icon = "🟢" if f["resisted"] else "🔴"
        dR_str = f"{f['dR']:+.4f}" if f["dR"] is not None else "N/A"
        print(f"    {icon} {f['domain']:18s} δR={dR_str:>8s}  {'устоял' if f['resisted'] else 'сломался'}")

    print(f"\n  Каскад (H2O):")
    for c in all_results["cascade"]:
        icon = "🟢" if c["correct"] else "🔴"
        nll_str = f"NLL={c['nll']:.4f}" if c["nll"] is not None else "NLL=N/A"
        print(f"    {icon} {c['n_lies']:2d} ложей → «{c['answer']:15s}» {nll_str}")

    print(f"\n  Каскад (14-й президент):")
    for c in all_results["cascade_hard"]:
        icon = "🟢" if c["correct"] else "🔴"
        nll_str = f"NLL={c['nll']:.4f}" if c["nll"] is not None else "NLL=N/A"
        print(f"    {icon} {c['n_lies']:2d} ложей → «{c['answer']:15s}» {nll_str}")

    with open(f"experiment_b_{MODEL.replace('.', '_').replace('-', '_')}_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 Сохранено в experiment_b_{MODEL}_results.json")


if __name__ == "__main__":
    print("🔬 Эксперимент B — OpenAI (несколько моделей)")
    print(f"   Модели: {', '.join(MODELS)}")
    print()
    
    for m in MODELS:
        MODEL = m
        print(f"\n{'#' * 60}")
        print(f"#  {MODEL}")
        print(f"{'#' * 60}")
        
        if phase1():
            print("\n  Logprobs работают. Запускаю эксперимент B...")
            run_experiment()
        else:
            print(f"\n  {MODEL}: Logprobs не доступны, пропускаю.")
        
        time.sleep(1)
