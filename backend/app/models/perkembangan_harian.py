from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class PerkembanganHarian(Base):
    """
    Model ORM untuk tabel 'perkembangan_harian' di database raport_tk.
    Menyimpan catatan dan observasi harian perkembangan siswa oleh guru pendamping.
    """
    __tablename__ = "perkembangan_harian"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("siswa.id"), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    behavior = Column(Text, nullable=True)
    social_interaction = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("pengguna.id"), nullable=True)

    # Relasi ke Siswa dan Pengguna
    student = relationship("Siswa", backref="daily_reports")
    creator = relationship("Pengguna", backref="daily_reports")

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
    def pembuat(self):
        return self.creator

    @pembuat.setter
    def pembuat(self, value):
        self.creator = value

    @property
    def tanggal(self):
        return self.date

    @tanggal.setter
    def tanggal(self, value):
        self.date = value

    @property
    def catatan(self) -> str:
        return self.notes

    @catatan.setter
    def catatan(self, value: str):
        self.notes = value

    @property
    def perilaku(self) -> str:
        return self.behavior

    @perilaku.setter
    def perilaku(self, value: str):
        self.behavior = value

    @property
    def interaksi_sosial(self) -> str:
        return self.social_interaction

    @interaksi_sosial.setter
    def interaksi_sosial(self, value: str):
        self.social_interaction = value

    @property
    def dibuat_oleh(self) -> int:
        return self.created_by

    @dibuat_oleh.setter
    def dibuat_oleh(self, value: int):
        self.created_by = value

    def __repr__(self):
        return f"<PerkembanganHarian(id={self.id}, student_id={self.student_id}, date='{self.date}')>"


# Alias untuk kompatibilitas kode lama
DailyReport = PerkembanganHarian
