from typing import List
from .models import TranscriptSegmentIn, Protocol, Quality, ScoreBlock, GreetingAndContact, NeedsAssessment, SubCriteria

WEIGHTS = {
    "структура_разговора_0_5": 5,
    "приветствие_и_контакт_0_3": 3,
    "выявление_потребности_0_4": 4,
    "семейный_анамнез_0_3": 3,
    "профилактика_и_факторы_риска_0_3": 3,
    "планирование_лечения_0_3": 3,
    "заключение_визита_0_3": 3,
}
MAX_SUM = sum(WEIGHTS.values())

def _evidence(seg: TranscriptSegmentIn) -> str:
    return f"[{seg.start:.1f}–{seg.end:.1f} {seg.speaker}] {seg.text.strip()}"

def score_quality(segments: List[TranscriptSegmentIn], protocol: Protocol) -> Quality:
    struct_evd = []
    greet_evd = []
    needs_evd = []
    fam_evd = []
    prev_evd = []
    plan_evd = []
    close_evd = []

    sub = SubCriteria()

    asked_complaints = False
    asked_history = False
    med_history = False
    drug_history = False
    did_plan = False
    did_close = False

    for s in segments:
        t = s.text.lower()
        if any(w in t for w in ["здравствуйте", "добрый день", "приветствую"]):
            sub.correct_greeting = 1
            greet_evd.append(_evidence(s))
        if "это врач" in t or "меня зовут" in t:
            sub.doctor_introduction = 1
            greet_evd.append(_evidence(s))
        if "как к вам обращаться" in t or "можно на" in t:
            sub.address_preference = 1
            greet_evd.append(_evidence(s))

        if "жалоб" in t:
            asked_complaints = True
            needs_evd.append(_evidence(s))
        if any(x in t for x in ["анамнез", "с какого времени", "с 27 лет", "давно ли"]):
            asked_history = True
            needs_evd.append(_evidence(s))
        if any(x in t for x in ["туберкул", "гепатит", "сахарный диабет", "хронические"]):
            med_history = True
            needs_evd.append(_evidence(s))
        if any(x in t for x in ["лекарств", "препарат", "сижу на лекарств"]):
            drug_history = True
            needs_evd.append(_evidence(s))

        if "предварительный диагноз" in t or "план" in t or "необходима консультация" in t:
            did_plan = True
            plan_evd.append(_evidence(s))

        if any(x in t for x in ["до свидания", "всего доброго", "спасибо"]):
            did_close = True
            close_evd.append(_evidence(s))

        if "давление" in t or "пульс" in t or "диагноз" in t:
            struct_evd.append(_evidence(s))

        if any(x in t for x in ["у родственников", "наследствен", "семейн"]):
            fam_evd.append(_evidence(s))
        if any(x in t for x in ["курите", "алкоголь", "факторы риска", "профилактик"]):
            prev_evd.append(_evidence(s))

    structure_score = 1 if (asked_complaints and did_plan and did_close) else 0
    needs_score = int(asked_complaints) + int(asked_history) + int(med_history) + int(drug_history)
    if needs_score > 4:
        needs_score = 4

    greeting_score = sub.correct_greeting + sub.doctor_introduction + sub.address_preference

    family_score = 1 if fam_evd else 0
    prevention_score = 1 if prev_evd else 0
    planning_score = 1 if did_plan else 0
    closing_score = 1 if did_close else 0

    weighted = (
        structure_score * WEIGHTS["структура_разговора_0_5"]
        + greeting_score * 1
        + needs_score * 1
        + family_score * WEIGHTS["семейный_анамнез_0_3"] / 3
        + prevention_score * WEIGHTS["профилактика_и_факторы_риска_0_3"] / 3
        + planning_score * WEIGHTS["планирование_лечения_0_3"] / 3
        + closing_score * WEIGHTS["заключение_визита_0_3"] / 3
    )
    total = int(round((weighted / MAX_SUM) * 100))

    quality = Quality(
        **{
            "итоговый_балл_0_100": max(0, min(100, total)),
            "структура_разговора_0_5": {"балл": int(structure_score), "доказательства": struct_evd},
            "приветствие_и_контакт_0_3": {
                "балл": int(greeting_score),
                "подкритерии": {
                    "корректное_приветствие": sub.correct_greeting,
                    "представление_врача": sub.doctor_introduction,
                    "уточнение_обращения": sub.address_preference,
                },
                "доказательства": greet_evd,
            },
            "выявление_потребности_0_4": {
                "балл": int(needs_score),
                "подкритерии": {
                    "текущие_жалобы": int(asked_complaints),
                    "анамнез_заболевания": int(asked_history),
                    "общий_медицинский_анамнез": int(med_history),
                    "лекарственный_анамнез": int(drug_history),
                },
                "доказательства": needs_evd,
            },
            "семейный_анамнез_0_3": {"балл": int(family_score), "доказательства": fam_evd},
            "профилактика_и_факторы_риска_0_3": {"балл": int(prevention_score), "доказательства": prev_evd},
            "планирование_лечения_0_3": {"балл": int(planning_score), "доказательства": plan_evd},
            "заключение_визита_0_3": {"балл": int(closing_score), "доказательства": close_evd},
        }
    )

    return quality
