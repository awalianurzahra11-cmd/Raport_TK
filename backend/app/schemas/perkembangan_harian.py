import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class PerkembanganHarianCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    student_id: int = Field(..., validation_alias=AliasChoices("student_id", "siswa_id"))
    date: datetime.date = Field(..., validation_alias=AliasChoices("date", "tanggal"))
    notes: Optional[str] = Field(None, validation_alias=AliasChoices("notes", "catatan"))
    behavior: Optional[str] = Field(None, validation_alias=AliasChoices("behavior", "perilaku"))
    social_interaction: Optional[str] = Field(None, validation_alias=AliasChoices("social_interaction", "interaksi_sosial"))


class PerkembanganHarianUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    notes: Optional[str] = Field(None, validation_alias=AliasChoices("notes", "catatan"))
    behavior: Optional[str] = Field(None, validation_alias=AliasChoices("behavior", "perilaku"))
    social_interaction: Optional[str] = Field(None, validation_alias=AliasChoices("social_interaction", "interaksi_sosial"))


class PerkembanganHarianOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    student_id: int
    date: datetime.date
    notes: Optional[str] = None
    behavior: Optional[str] = None
    social_interaction: Optional[str] = None
    created_by: Optional[int] = None


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
DailyReportCreate = PerkembanganHarianCreate
DailyReportUpdate = PerkembanganHarianUpdate
DailyReportOut = PerkembanganHarianOut
