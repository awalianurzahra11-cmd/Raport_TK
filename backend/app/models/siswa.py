from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base


class Siswa(Base):
    """
    Model ORM untuk tabel 'siswa' di database raport_tk.
    Menyimpan data anak didik berkebutuhan khusus (ABK).
    """
    __tablename__ = "siswa"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    age = Column(Integer, nullable=False, default=0)
    birth_date = Column(String(50), nullable=True)
    special_needs = Column(String(255), nullable=True)
    class_name = Column(String(50), nullable=True)
    teacher_id = Column(Integer, ForeignKey("pengguna.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke Pengguna (Guru Pendamping)
    teacher = relationship("Pengguna", foreign_keys=[teacher_id], backref="students")

    # ── Property Alias Bahasa Indonesia ──────────────────────────────
    @property
    def guru(self):
        return self.teacher

    @guru.setter
    def guru(self, value):
        self.teacher = value

    @property
    def nama(self) -> str:
        return self.name

    @nama.setter
    def nama(self, value: str):
        self.name = value

    @property
    def usia(self) -> int:
        return self.age

    @usia.setter
    def usia(self, value: int):
        self.age = value

    @property
    def tanggal_lahir(self) -> str:
        return self.birth_date

    @tanggal_lahir.setter
    def tanggal_lahir(self, value: str):
        self.birth_date = value

    @property
    def kebutuhan_khusus(self) -> str:
        return self.special_needs

    @kebutuhan_khusus.setter
    def kebutuhan_khusus(self, value: str):
        self.special_needs = value

    @property
    def nama_kelas(self) -> str:
        return self.class_name

    @nama_kelas.setter
    def nama_kelas(self, value: str):
        self.class_name = value

    @property
    def guru_id(self) -> int:
        return self.teacher_id

    @guru_id.setter
    def guru_id(self, value: int):
        self.teacher_id = value

    @property
    def dibuat_pada(self):
        return self.created_at

    def __repr__(self):
        return f"<Siswa(id={self.id}, name='{self.name}', class_name='{self.class_name}')>"


# Alias untuk kompatibilitas kode lama
Student = Siswa
