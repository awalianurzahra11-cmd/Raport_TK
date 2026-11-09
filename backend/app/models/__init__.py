from .pengguna import Pengguna, User, UserRole, PeranPengguna
from .siswa import Siswa, Student
from .perkembangan_harian import PerkembanganHarian, DailyReport
from .raport import Raport, Assessment
from .input_penilaian import InputPenilaian, Evaluation
from .galeri_kegiatan import GaleriKegiatan, Gallery

__all__ = [
    # Model Utama Bahasa Indonesia
    "Pengguna",
    "Siswa",
    "PerkembanganHarian",
    "Raport",
    "InputPenilaian",
    "GaleriKegiatan",
    "PeranPengguna",
    # Alias Kompatibilitas Bahasa Inggris
    "User",
    "Student",
    "DailyReport",
    "Assessment",
    "Evaluation",
    "Gallery",
    "UserRole",
]
