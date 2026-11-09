from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from datetime import datetime


class RaportCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    student_id: int = Field(..., validation_alias=AliasChoices("student_id", "siswa_id"))
    period: str = Field(..., validation_alias=AliasChoices("period", "periode"))
    motoric: Optional[str] = Field(None, validation_alias=AliasChoices("motoric", "motorik"))
    language: Optional[str] = Field(None, validation_alias=AliasChoices("language", "bahasa"))
    social: Optional[str] = Field(None, validation_alias=AliasChoices("social", "sosial", "social_emotional", "sosial_emosional"))
    cognitive: Optional[str] = Field(None, validation_alias=AliasChoices("cognitive", "kognitif"))
    independence: Optional[str] = Field(None, validation_alias=AliasChoices("independence", "kemandirian"))
    summary: Optional[str] = Field(None, validation_alias=AliasChoices("summary", "kesimpulan", "ringkasan"))


class RaportUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    period: Optional[str] = Field(None, validation_alias=AliasChoices("period", "periode"))
    motoric: Optional[str] = Field(None, validation_alias=AliasChoices("motoric", "motorik"))
    language: Optional[str] = Field(None, validation_alias=AliasChoices("language", "bahasa"))
    social: Optional[str] = Field(None, validation_alias=AliasChoices("social", "sosial", "social_emotional", "sosial_emosional"))
    cognitive: Optional[str] = Field(None, validation_alias=AliasChoices("cognitive", "kognitif"))
    independence: Optional[str] = Field(None, validation_alias=AliasChoices("independence", "kemandirian"))
    summary: Optional[str] = Field(None, validation_alias=AliasChoices("summary", "kesimpulan", "ringkasan"))


class RaportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    student_id: int
    period: str
    motoric: Optional[str] = None
    language: Optional[str] = None
    social: Optional[str] = None
    cognitive: Optional[str] = None
    independence: Optional[str] = None
    summary: Optional[str] = None
    created_at: Optional[datetime] = None


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
AssessmentCreate = RaportCreate
AssessmentUpdate = RaportUpdate
AssessmentOut = RaportOut
