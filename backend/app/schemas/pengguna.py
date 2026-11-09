from pydantic import BaseModel, EmailStr, ConfigDict, Field, AliasChoices
from enum import Enum
from typing import Optional


class PeranPengguna(str, Enum):
    admin = "admin"
    pendamping = "pendamping"


class PenggunaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(..., validation_alias=AliasChoices("name", "nama"))
    email: EmailStr
    password: str = Field(..., validation_alias=AliasChoices("password", "kata_sandi"))
    role: PeranPengguna = Field(
        PeranPengguna.pendamping,
        validation_alias=AliasChoices("role", "peran")
    )


class PenggunaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    email: str
    role: PeranPengguna


class PenggunaLogin(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    password: str = Field(..., validation_alias=AliasChoices("password", "kata_sandi"))


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Alias Kompatibilitas Kode Lama ──────────────────────────────────
UserRole = PeranPengguna
UserCreate = PenggunaCreate
UserOut = PenggunaOut
UserLogin = PenggunaLogin
