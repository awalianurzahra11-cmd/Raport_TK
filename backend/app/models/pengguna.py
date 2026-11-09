from sqlalchemy import Column, Integer, String, Enum
from backend.app.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    pendamping = "pendamping"

    def __str__(self):
        return self.value


# Alias bahasa Indonesia untuk enum peran
PeranPengguna = UserRole


class Pengguna(Base):
    """
    Model ORM untuk tabel 'pengguna' di database raport_tk.
    Menyimpan data akun sistem (Admin dan Guru Pendamping).
    """
    __tablename__ = "pengguna"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.pendamping, nullable=False)

    # ── Property Alias Bahasa Indonesia ──────────────────────────────
    @property
    def nama(self) -> str:
        return self.name

    @nama.setter
    def nama(self, value: str):
        self.name = value

    @property
    def peran(self) -> UserRole:
        return self.role

    @peran.setter
    def peran(self, value: UserRole):
        self.role = value

    @property
    def kata_sandi_hash(self) -> str:
        return self.hashed_password

    @kata_sandi_hash.setter
    def kata_sandi_hash(self, value: str):
        self.hashed_password = value

    def __repr__(self):
        return f"<Pengguna(id={self.id}, name='{self.name}', role='{self.role}')>"


# Alias untuk kompatibilitas kode lama
User = Pengguna
