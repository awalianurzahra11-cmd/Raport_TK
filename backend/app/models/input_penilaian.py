from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database import Base


class InputPenilaian(Base):
    """
    Model ORM untuk tabel 'input_penilaian' di database raport_tk.
    Menyimpan data evaluasi instrumen kuantitatif BK (Bimbingan Konseling) per ranah dan skor komposit.
    """
    __tablename__ = "input_penilaian"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("siswa.id"), nullable=False)
    date = Column(Date, nullable=False)
    class_name = Column(String(50), nullable=True)
    diagnosa = Column(String(255), nullable=True)

    # JSON string berisi skor per indikator (misal {"c1": 4, "m1": 3, ...})
    scores = Column(Text, nullable=True)

    # Rata-rata Ranah (Skala 1.0 - 4.0)
    avg_cognitive = Column(Float, nullable=True)
    avg_motoric = Column(Float, nullable=True)
    avg_language = Column(Float, nullable=True)
    avg_social = Column(Float, nullable=True)
    avg_independence = Column(Float, nullable=True)

    # Indeks Komposit & Predikat
    composite_index = Column(Float, nullable=True)
    index_percentage = Column(Float, nullable=True)
    predicate = Column(String(10), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi ke Siswa
    student = relationship("Siswa", backref="evaluations")

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
    def tanggal(self):
        return self.date

    @tanggal.setter
    def tanggal(self, value):
        self.date = value

    @property
    def nama_kelas(self) -> str:
        return self.class_name

    @nama_kelas.setter
    def nama_kelas(self, value: str):
        self.class_name = value

    @property
    def skor(self) -> str:
        return self.scores

    @skor.setter
    def skor(self, value: str):
        self.scores = value

    @property
    def rata_kognitif(self) -> float:
        return self.avg_cognitive

    @rata_kognitif.setter
    def rata_kognitif(self, value: float):
        self.avg_cognitive = value

    @property
    def rata_motorik(self) -> float:
        return self.avg_motoric

    @rata_motorik.setter
    def rata_motorik(self, value: float):
        self.avg_motoric = value

    @property
    def rata_bahasa(self) -> float:
        return self.avg_language

    @rata_bahasa.setter
    def rata_bahasa(self, value: float):
        self.avg_language = value

    @property
    def rata_sosial(self) -> float:
        return self.avg_social

    @rata_sosial.setter
    def rata_sosial(self, value: float):
        self.avg_social = value

    @property
    def rata_kemandirian(self) -> float:
        return self.avg_independence

    @rata_kemandirian.setter
    def rata_kemandirian(self, value: float):
        self.avg_independence = value

    @property
    def indeks_komposit(self) -> float:
        return self.composite_index

    @indeks_komposit.setter
    def indeks_komposit(self, value: float):
        self.composite_index = value

    @property
    def persentase_indeks(self) -> float:
        return self.index_percentage

    @persentase_indeks.setter
    def persentase_indeks(self, value: float):
        self.index_percentage = value

    @property
    def predikat(self) -> str:
        return self.predicate

    @predikat.setter
    def predikat(self, value: str):
        self.predicate = value

    @property
    def dibuat_pada(self):
        return self.created_at

    def __repr__(self):
        return f"<InputPenilaian(id={self.id}, student_id={self.student_id}, predicate='{self.predicate}')>"


# Alias untuk kompatibilitas kode lama
Evaluation = InputPenilaian
