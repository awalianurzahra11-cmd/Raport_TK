import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class GaleriKegiatanCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    student_id: int = Field(..., validation_alias=AliasChoices("student_id", "siswa_id"))
    image_path: str = Field(..., validation_alias=AliasChoices("image_path", "jalur_gambar"))
    description: Optional[str] = Field(None, validation_alias=AliasChoices("description", "deskripsi"))
    domain: Optional[str] = Field(None, validation_alias=AliasChoices("domain", "ranah"))
    date: datetime.date = Field(..., validation_alias=AliasChoices("date", "tanggal"))


class GaleriKegiatanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    student_id: int
    image_path: str
    description: Optional[str] = None
    domain: Optional[str] = None
    date: datetime.date


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
GalleryOut = GaleriKegiatanOut
GalleryCreate = GaleriKegiatanCreate
