from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class GaleriKegiatan(Base):
    """
    Model ORM untuk tabel 'galeri_kegiatan' di database raport_tk.
    Menyimpan dokumentasi foto kegiatan belajar dan observasi siswa.
    """
    __tablename__ = "galeri_kegiatan"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("siswa.id"), nullable=False)
    image_path = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(100), nullable=True)
    date = Column(Date, nullable=False)

    # Relasi ke Siswa
    student = relationship("Siswa", backref="gallery_items")

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
    def jalur_gambar(self) -> str:
        return self.image_path

    @jalur_gambar.setter
    def jalur_gambar(self, value: str):
        self.image_path = value

    @property
    def deskripsi(self) -> str:
        return self.description

    @deskripsi.setter
    def deskripsi(self, value: str):
        self.description = value

    @property
    def ranah(self) -> str:
        return self.domain

    @ranah.setter
    def ranah(self, value: str):
        self.domain = value

    @property
    def tanggal(self):
        return self.date

    @tanggal.setter
    def tanggal(self, value):
        self.date = value

    def __repr__(self):
        return f"<GaleriKegiatan(id={self.id}, student_id={self.student_id}, image_path='{self.image_path}')>"


# Alias untuk kompatibilitas kode lama
Gallery = GaleriKegiatan
