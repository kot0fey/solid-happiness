import re
from typing import Optional

def parse_height_cm(text: str) -> Optional[float]:
    if not text:
        return None
    t = text.lower().replace(",", ".")
    m = re.search(r"(\d+[.,]?\d*)\s*м\s*(\d{1,3})?", t)
    if m:
        meters = float(m.group(1))
        cm_extra = float(m.group(2)) if m.group(2) else 0.0
        return round(meters * 100 + cm_extra, 2)
    m = re.search(r"(\d{2,3})\s*см", t)
    if m:
        return float(m.group(1))
    m = re.search(r"\b(1\.?\d{2})\b", t)
    if m:
        return round(float(m.group(1)) * 100, 2)
    return None

def parse_weight_kg(text: str) -> Optional[float]:
    if not text:
        return None
    t = text.lower().replace(",", ".")
    m = re.search(r"(\d+[.,]?\d*)\s*кг", t)
    if m:
        return float(m.group(1))
    return None

def parse_spo2(text: str) -> Optional[float]:
    if not text:
        return None
    t = text.lower()
    m = re.search(r"(spo2|сатурац)[^\d]{0,5}(\d{2,3})\s*%?", t)
    if m:
        return float(m.group(2))
    m = re.search(r"\b(\d{2,3})\s*%\b", t)
    if m and 80 <= int(m.group(1)) <= 100:
        return float(m.group(1))
    return None

def parse_bp_systolic(text: str) -> Optional[float]:
    if not text:
        return None
    t = text.lower()
    m = re.search(r"(\d{2,3})\s*(?:/|на)\s*(\d{2,3})", t)
    if m:
        return float(m.group(1))
    m = re.search(r"систолическ[^\d]{0,5}(\d{2,3})", t)
    if m:
        return float(m.group(1))
    return None

def calc_bmi(weight_kg: Optional[float], height_cm: Optional[float]) -> Optional[float]:
    if weight_kg and height_cm and height_cm > 0:
        h_m = height_cm / 100.0
        return weight_kg / (h_m ** 2)
    return None
