from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base


class Raport(Base):
    """
    Model ORM untuk tabel 'raport' di database raport_tk.
    Menyimpan laporan naratif berkala perkembangan anak per ranah (Motorik, Bahasa, Sosial, Kognitif, Kemandirian).
    """
    __tablename__ = "raport"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("siswa.id"), nullable=False)
    period = Column(String(50), nullable=False)  # Contoh: "Semester 1 2025/2026"
    motoric = Column(Text, nullable=True)
    language = Column(Text, nullable=True)
    social = Column(Text, nullable=True)
    cognitive = Column(Text, nullable=True)
    independence = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke Siswa
    student = relationship("Siswa", backref="assessments")

    # ── Property Alias Bahasa Indonesia ──────────────────────────────
    @property
    def siswa_id(self) -> int:
        return self.student_id

    @siswa_id.setter
    def siswa_id(self, value: int):
        self.student_id = value

    @property
    def siswa(self):
        return self.student

    @siswa.setter
    def siswa(self, value):
        self.student = value

    @property
    def periode(self) -> str:
        return self.period

    @periode.setter
    def periode(self, value: str):
        self.period = value

    @property
    def motorik(self) -> str:
        return self.motoric

    @motorik.setter
    def motorik(self, value: str):
        self.motoric = value

    @property
    def bahasa(self) -> str:
        return self.language

    @bahasa.setter
    def bahasa(self, value: str):
        self.language = value

    @property
    def sosial(self) -> str:
        return self.social

    @sosial.setter
    def sosial(self, value: str):
        self.social = value

    # Alias alternatif untuk social_emotional
    @property
    def social_emotional(self) -> str:
        return self.social

    @social_emotional.setter
    def social_emotional(self, value: str):
        self.social = value

    @property
    def sosial_emosional(self) -> str:
        return self.social

    @sosial_emosional.setter
    def sosial_emosional(self, value: str):
        self.social = value

    @property
    def kognitif(self) -> str:
        return self.cognitive

    @kognitif.setter
    def kognitif(self, value: str):
        self.cognitive = value

    @property
    def kemandirian(self) -> str:
        return self.independence

    @kemandirian.setter
    def kemandirian(self, value: str):
        self.independence = value

    @property
    def kesimpulan(self) -> str:
        return self.summary

    @kesimpulan.setter
    def kesimpulan(self, value: str):
        self.summary = value

    @property
    def ringkasan(self) -> str:
        return self.summary

    @ringkasan.setter
    def ringkasan(self, value: str):
        self.summary = value

    @property
    def dibuat_pada(self):
        return self.created_at

    def __repr__(self):
        return f"<Raport(id={self.id}, student_id={self.student_id}, period='{self.period}')>"


# Alias untuk kompatibilitas kode lama
Assessment = Raport
