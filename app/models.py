from pydantic import BaseModel, Field
from typing import List, Optional

class TranscriptSegmentIn(BaseModel):
    start: float
    end: float
    speaker: str
    text: str

class BMI(BaseModel):
    value: Optional[float] = Field(None, alias="значение")

    class Config:
        populate_by_name = True
        json_encoders = {float: lambda v: round(v, 2) if v is not None else None}

class Protocol(BaseModel):
    complaints: Optional[str] = Field(None, alias="жалобы")
    anamnesis: Optional[str] = Field(None, alias="анамнез")
    diagnosis: Optional[str] = Field(None, alias="диагноз")
    treatment_plan: Optional[str] = Field(None, alias="план_лечения")
    patient_advice: List[str] = Field(default_factory=list, alias="рекомендации_пациенту")
    height_cm: Optional[float] = Field(None, alias="рост_см")
    weight_kg: Optional[float] = Field(None, alias="вес_кг")
    spo2_pct: Optional[float] = Field(None, alias="сатурация_проц")
    systolic_bp: Optional[float] = Field(None, alias="систолическое_давление_ммртст")
    bmi: BMI = Field(default_factory=BMI, alias="ИМТ")

    class Config:
        populate_by_name = True
        json_encoders = {float: lambda v: round(v, 2) if v is not None else None}

class SubCriteria(BaseModel):
    correct_greeting: int = Field(0, alias="корректное_приветствие")
    doctor_introduction: int = Field(0, alias="представление_врача")
    address_preference: int = Field(0, alias="уточнение_обращения")

    class Config:
        populate_by_name = True

class ScoreBlock(BaseModel):
    score: int = Field(0, alias="балл")
    evidence: List[str] = Field(default_factory=list, alias="доказательства")

    class Config:
        populate_by_name = True

class GreetingAndContact(BaseModel):
    score: int = Field(0, alias="балл")
    sub: SubCriteria = Field(default_factory=SubCriteria, alias="подкритерии")
    evidence: List[str] = Field(default_factory=list, alias="доказательства")

    class Config:
        populate_by_name = True

class NeedsAssessment(BaseModel):
    score: int = Field(0, alias="балл")
    sub_current: int = Field(0, alias="текущие_жалобы")
    sub_disease_anamnesis: int = Field(0, alias="анамнез_заболевания")
    sub_med_anamnesis: int = Field(0, alias="общий_медицинский_анамнез")
    sub_drug_anamnesis: int = Field(0, alias="лекарственный_анамнез")
    evidence: List[str] = Field(default_factory=list, alias="доказательства")

    class Config:
        populate_by_name = True

class Quality(BaseModel):
    total_0_100: int = Field(0, alias="итоговый_балл_0_100")
    structure_0_5: ScoreBlock = Field(default_factory=ScoreBlock, alias="структура_разговора_0_5")
    greeting_0_3: GreetingAndContact = Field(default_factory=GreetingAndContact, alias="приветствие_и_контакт_0_3")
    needs_0_4: NeedsAssessment = Field(default_factory=NeedsAssessment, alias="выявление_потребности_0_4")
    family_0_3: ScoreBlock = Field(default_factory=ScoreBlock, alias="семейный_анамнез_0_3")
    prevention_0_3: ScoreBlock = Field(default_factory=ScoreBlock, alias="профилактика_и_факторы_риска_0_3")
    planning_0_3: ScoreBlock = Field(default_factory=ScoreBlock, alias="планирование_лечения_0_3")
    closing_0_3: ScoreBlock = Field(default_factory=ScoreBlock, alias="заключение_визита_0_3")

    class Config:
        populate_by_name = True

class VisitResponse(BaseModel):
    protocol: Protocol = Field(alias="протокол")
    quality: Quality = Field(alias="качество")

    class Config:
        populate_by_name = True







# ---------------------------
# Блок данных осмотра
# ---------------------------
class ExamData(BaseModel):
    complaints: Optional[str]                      # Жалобы пациента
    anamnesis: Optional[str]                       # Анамнез заболевания
    diagnosis: Optional[str]                       # Диагноз
    treatment_plan: Optional[str]                  # План лечения
    patient_recommendations: Optional[str]         # Рекомендации пациенту


# ---------------------------
# Показатели (виталые)
# ---------------------------
class Vitals(BaseModel):
    height_cm: Optional[float]           # Рост (см)
    weight_kg: Optional[float]           # Вес (кг)
    bmi: Optional[float]                 # Индекс массы тела
    waist_height_ratio: Optional[float]  # Индекс талия/рост
    pulse: Optional[int]                 # Пульс
    spo2: Optional[int]                  # Сатурация
    systolic_bp: Optional[str]           # Систолическое давление (строка "120/80")


# ---------------------------
# Критерии качества консультации
# ---------------------------
class QualityCriteria(BaseModel):
    greeting_and_contact: int
    conversation_structure: int
    needs_identification: int
    current_complaints_identification: int
    disease_history: int
    general_medical_history: int
    medication_history: int
    family_history: int
    prevention_and_risk_control: int
    treatment_planning: int
    visit_closure: int


# ---------------------------
# Качество обследования
# ---------------------------
class ExaminationQuality(BaseModel):
    overall_score: Optional[float]          # Общая оценка
    criteria_completed: Optional[int]       # Критериев выполнено
    criteria_total: Optional[int]           # Всего критериев


# ---------------------------
# Аналитика диалога
# ---------------------------
class DialogueAnalytics(BaseModel):
    doctor_showed_empathy: int
    doctor_interrupted_patient: int
    patient_asked_questions: int
    doctor_used_medical_jargon: int
    doctor_confirmed_understanding: int
    lifestyle_discussed: int
    allergies_discussed: int
    shared_decision_making: int
    patient_compliance_assessment: int
    doctor_pacing: int


# ---------------------------
# СППВР (Clinical Decision Support)
# ---------------------------
class ClinicalDecisionSupport(BaseModel):
    quality_criteria: QualityCriteria       # Критерии качества
    examination_quality: ExaminationQuality # Качество обследования
    dialogue_analytics: DialogueAnalytics   # Аналитика диалога


# ---------------------------
# Основная модель ответа backend
# ---------------------------
class BackendResponse(BaseModel):
    exam_data: ExamData
    vitals: Vitals
    clinical_decision_support: ClinicalDecisionSupport