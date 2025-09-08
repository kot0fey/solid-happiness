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
