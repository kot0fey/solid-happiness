from typing import List, Dict
from .models import TranscriptSegmentIn, Protocol
from .normalization import (
    parse_height_cm, parse_weight_kg, parse_spo2,
    parse_bp_systolic, calc_bmi
)
from .llm import call_llm
import json

def build_protocol_from_segments(segments: List[TranscriptSegmentIn]) -> Dict:
    text_all = " ".join(s.text for s in segments)

    height = parse_height_cm(text_all)
    weight = parse_weight_kg(text_all)
    spo2 = parse_spo2(text_all)
    bp = parse_bp_systolic(text_all)
    bmi_val = calc_bmi(weight, height)

    protocol = Protocol(
        complaints=None,
        anamnesis=None,
        diagnosis=None,
        treatment_plan=None,
        patient_advice=[],
        height_cm=height,
        weight_kg=weight,
        spo2_pct=spo2,
        systolic_bp=bp,
        bmi={"значение": bmi_val} if bmi_val else {"значение": None}
    ).dict(by_alias=True)

    try:
        joined = "\n".join(f"{s.speaker}: {s.text}" for s in segments)
        prompt = f"""
Ты медицинский ассистент. Твоя задача – извлечь из транскрипта консультации врача и пациента структурированные данные по заданной схеме.

Правила:
- Строго возвращай JSON только по схеме ниже, без лишнего текста и комментариев.
- Если данные отсутствуют в транскрипте → ставь null.
- Если данные присутствуют, но не названы явно, а только косвенно (например, "похоже на бронхит") → фиксируй это как диагноз/анамнез/жалобу в явном виде.
- Рекомендации врача всегда разбивай в массив отдельных коротких строк (даже если они даны слитно).
- Числовые поля (рост, вес, давление, сатурация) указывай только если в транскрипте есть конкретные цифры. Никогда не придумывай значения.
- Для "ИМТ.значение" вычисляй индекс массы тела, если известны рост и вес. Если одного из параметров нет, ставь null.

Сформируй JSON строго по схеме:
{{
  "жалобы": string|null,
  "анамнез": string|null,
  "диагноз": string|null,
  "план_лечения": string|null,
  "рекомендации_пациенту": [string],
  "рост_см": number|null,
  "вес_кг": number|null,
  "сатурация_проц": number|null,
  "систолическое_давление_ммртст": number|null,
  "ИМТ": {{"значение": number|null}}
}}
 На входе транскрипт консультации врача и пациента:
---
{joined}
---
Не придумывай данные, если в транскрипте их нет.
        """
        llm_out = call_llm(prompt)
        parsed = json.loads(llm_out)
        protocol.update({k: v for k, v in parsed.items() if k in protocol})
    except Exception:
        pass

    return protocol
