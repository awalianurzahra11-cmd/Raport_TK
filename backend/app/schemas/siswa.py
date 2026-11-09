from pydantic import BaseModel, ConfigDict, Field, AliasChoices
from typing import Optional
from datetime import datetime


class SiswaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(..., validation_alias=AliasChoices("name", "nama"))
    age: int = Field(0, validation_alias=AliasChoices("age", "usia"))
    birth_date: Optional[str] = Field(None, validation_alias=AliasChoices("birth_date", "tanggal_lahir"))
    special_needs: Optional[str] = Field(None, validation_alias=AliasChoices("special_needs", "kebutuhan_khusus"))
    class_name: Optional[str] = Field(None, validation_alias=AliasChoices("class_name", "nama_kelas"))


class SiswaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: Optional[str] = Field(None, validation_alias=AliasChoices("name", "nama"))
    age: Optional[int] = Field(None, validation_alias=AliasChoices("age", "usia"))
    birth_date: Optional[str] = Field(None, validation_alias=AliasChoices("birth_date", "tanggal_lahir"))
    special_needs: Optional[str] = Field(None, validation_alias=AliasChoices("special_needs", "kebutuhan_khusus"))
    class_name: Optional[str] = Field(None, validation_alias=AliasChoices("class_name", "nama_kelas"))


class SiswaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    age: int
    birth_date: Optional[str] = None
    special_needs: Optional[str] = None
    class_name: Optional[str] = None
    created_at: Optional[datetime] = None


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
StudentCreate = SiswaCreate
StudentUpdate = SiswaUpdate
StudentOut = SiswaOut
