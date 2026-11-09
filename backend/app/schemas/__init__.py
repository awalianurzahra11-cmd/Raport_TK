from .pengguna import (
    PenggunaCreate, PenggunaOut, PenggunaLogin, PeranPengguna, Token,
    UserCreate, UserOut, UserLogin, UserRole
)
from .siswa import (
    SiswaCreate, SiswaUpdate, SiswaOut,
    StudentCreate, StudentUpdate, StudentOut
)
from .perkembangan_harian import (
    PerkembanganHarianCreate, PerkembanganHarianUpdate, PerkembanganHarianOut,
    DailyReportCreate, DailyReportUpdate, DailyReportOut
)
from .raport import (
    RaportCreate, RaportUpdate, RaportOut,
    AssessmentCreate, AssessmentUpdate, AssessmentOut
)
from .input_penilaian import (
    InputPenilaianCreate, InputPenilaianOut,
    EvaluationCreate, EvaluationOut
)
from .galeri_kegiatan import (
    GaleriKegiatanCreate, GaleriKegiatanOut,
    GalleryCreate, GalleryOut
)

__all__ = [
    # Schemas Bahasa Indonesia
    "PenggunaCreate", "PenggunaOut", "PenggunaLogin", "PeranPengguna", "Token",
    "SiswaCreate", "SiswaUpdate", "SiswaOut",
    "PerkembanganHarianCreate", "PerkembanganHarianUpdate", "PerkembanganHarianOut",
    "RaportCreate", "RaportUpdate", "RaportOut",
    "InputPenilaianCreate", "InputPenilaianOut",
    "GaleriKegiatanCreate", "GaleriKegiatanOut",
    # Backward Compatibility (English)
    "UserCreate", "UserOut", "UserLogin", "UserRole",
    "StudentCreate", "StudentUpdate", "StudentOut",
    "DailyReportCreate", "DailyReportUpdate", "DailyReportOut",
    "AssessmentCreate", "AssessmentUpdate", "AssessmentOut",
    "EvaluationCreate", "EvaluationOut",
    "GalleryCreate", "GalleryOut",
]
