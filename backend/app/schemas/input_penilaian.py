import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class InputPenilaianCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    student_id: int = Field(..., validation_alias=AliasChoices("student_id", "siswa_id"))
    date: datetime.date = Field(..., validation_alias=AliasChoices("date", "tanggal"))
    class_name: Optional[str] = Field(None, validation_alias=AliasChoices("class_name", "nama_kelas"))
    diagnosa: Optional[str] = None
    scores: Optional[str] = Field(None, validation_alias=AliasChoices("scores", "skor"))
    avg_cognitive: Optional[float] = Field(None, validation_alias=AliasChoices("avg_cognitive", "rata_kognitif"))
    avg_motoric: Optional[float] = Field(None, validation_alias=AliasChoices("avg_motoric", "rata_motorik"))
    avg_language: Optional[float] = Field(None, validation_alias=AliasChoices("avg_language", "rata_bahasa"))
    avg_social: Optional[float] = Field(None, validation_alias=AliasChoices("avg_social", "rata_sosial"))
    avg_independence: Optional[float] = Field(None, validation_alias=AliasChoices("avg_independence", "rata_kemandirian"))
    composite_index: Optional[float] = Field(None, validation_alias=AliasChoices("composite_index", "indeks_komposit"))
    index_percentage: Optional[float] = Field(None, validation_alias=AliasChoices("index_percentage", "persentase_indeks"))
    predicate: Optional[str] = Field(None, validation_alias=AliasChoices("predicate", "predikat"))


class InputPenilaianOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    student_id: int
    date: datetime.date
    class_name: Optional[str] = None
    diagnosa: Optional[str] = None
    scores: Optional[str] = None
    avg_cognitive: Optional[float] = None
    avg_motoric: Optional[float] = None
    avg_language: Optional[float] = None
    avg_social: Optional[float] = None
    avg_independence: Optional[float] = None
    composite_index: Optional[float] = None
    index_percentage: Optional[float] = None
    predicate: Optional[str] = None
    created_at: Optional[datetime.datetime] = None


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
EvaluationCreate = InputPenilaianCreate
EvaluationOut = InputPenilaianOut
