"""
Skrip Generator Dokumen PDF Dokumentasi Lengkap E-Raport TK
Membuat 2 File PDF:
1. Dokumentasi_Backend_E_Raport_TK.pdf
2. Dokumentasi_Frontend_E_Raport_TK.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ── CANVAS KHUSUS DENGAN RUNNING HEADER & NOMOR HALAMAN DINAMIS ──
class NumberedCanvas(canvas.Canvas):
    doc_title = "Dokumentasi Sistem E-Raport TK Inklusi ABK"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                
                # Header Running
                self.setFont('Helvetica-Bold', 8)
                self.setFillColor(colors.HexColor('#1e40af'))
                self.drawString(45, 842 - 32, self.doc_title)
                
                self.setFont('Helvetica', 8)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawRightString(595 - 45, 842 - 32, "Tugas Akhir / Skripsi")
                
                # Garis pemisah header
                self.setStrokeColor(colors.HexColor('#cbd5e1'))
                self.setLineWidth(0.5)
                self.line(45, 842 - 36, 595 - 45, 842 - 36)
                
                # Footer Running
                self.line(45, 42, 595 - 45, 42)
                self.setFont('Helvetica', 8)
                self.setFillColor(colors.HexColor('#64748b'))
                self.drawString(45, 30, "Sistem E-Raport TK Inklusi Anak Berkebutuhan Khusus")
                page_str = f"Halaman {self._pageNumber} dari {num_pages}"
                self.drawRightString(595 - 45, 30, page_str)
                
                self.restoreState()
            super().showPage()
        super().save()

class BackendNumberedCanvas(NumberedCanvas):
    doc_title = "Dokumentasi Backend — Sistem E-Raport TK Inklusi ABK"

class FrontendNumberedCanvas(NumberedCanvas):
    doc_title = "Dokumentasi Frontend — Sistem E-Raport TK Inklusi ABK"



def create_styles():
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1, # Center
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        name='CoverMeta',
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        alignment=1,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='BabTitle',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='SubBabTitle',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='SubSubBabTitle',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='BodyCustom',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='BulletCustom',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name='CodeBox',
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#0f172a'),
        backColor=colors.HexColor('#f8fafc'),
        borderColor=colors.HexColor('#e2e8f0'),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=4
    ))
    styles.add(ParagraphStyle(
        name='CalloutBox',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e40af'),
        backColor=colors.HexColor('#eff6ff'),
        borderColor=colors.HexColor('#bfdbfe'),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=4
    ))
    styles.add(ParagraphStyle(
        name='TableHead',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1e293b')
    ))
    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0f172a')
    ))
    return styles


# ── FUNGSI GENERATOR PDF BACKEND ──
def generate_backend_pdf(filename):
    print(f"[1/2] Membuat dokumen PDF Backend: {filename} ...")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    styles = create_styles()
    story = []

    # ── COVER PAGE ──
    story.append(Spacer(1, 40))
    story.append(Paragraph("DOKUMENTASI TEKNIS KODE SUMBER", styles['CoverSubtitle']))
    story.append(Paragraph("SISTEM E-RAPORT TK INKLUSI ABK<br/>(BACKEND ARCHITECTURE)", styles['CoverTitle']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="60%", thickness=2, color=colors.HexColor('#1e40af'), spaceBefore=10, spaceAfter=20))
    story.append(Paragraph("<b>Modul Analisis Arsitektur, Basis Data, Skema Validasi, Router API, Algoritma Penilaian BK, dan Keamanan Sistem</b>", styles['CoverSubtitle']))
    story.append(Spacer(1, 60))
    
    # Kotak Info Penulis & Sistem
    cover_table_data = [
        [Paragraph("<b>Topik Penelitian / Proyek:</b>", styles['TableCellBold']), Paragraph("Pengembangan Aplikasi Pelaporan Perkembangan Siswa TK Inklusi", styles['TableCell'])],
        [Paragraph("<b>Teknologi Inti Backend:</b>", styles['TableCellBold']), Paragraph("Python 3.10+, FastAPI, SQLAlchemy ORM, MySQL (Laragon)", styles['TableCell'])],
        [Paragraph("<b>Metode Autentikasi:</b>", styles['TableCellBold']), Paragraph("JWT (JSON Web Token) HS256 & Bcrypt Password Hashing", styles['TableCell'])],
        [Paragraph("<b>Standar Validasi Data:</b>", styles['TableCellBold']), Paragraph("Pydantic v2 dengan Skema Dwi-Bahasa (Indonesia & Inggris)", styles['TableCell'])],
        [Paragraph("<b>Format Dokumen:</b>", styles['TableCellBold']), Paragraph("Buku Dokumentasi Teknis Kode Sumber Tugas Akhir (Skripsi)", styles['TableCell'])],
        [Paragraph("<b>Status Sistem:</b>", styles['TableCellBold']), Paragraph("Produksi / Siap Uji (Production Ready - 82 Rute Aktif)", styles['TableCell'])],
    ]
    t_cover = Table(cover_table_data, colWidths=[180, 310])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 70))
    story.append(Paragraph("<b>TK INKLUSI KASIH ANAK BANGSA</b><br/>Tahun Akademik 2025/2026", styles['CoverMeta']))
    story.append(PageBreak())

    # ── DAFTAR ISI ──
    story.append(Paragraph("DAFTAR ISI DOKUMENTASI BACKEND", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=4, spaceAfter=12))
    
    daftar_isi = [
        ("BAB I", "Arsitektur Sistem & Gambaran Umum Backend", "Pilihan framework, struktur direktori, lifecyle, middleware SPA, dan CORS."),
        ("BAB II", "Struktur Basis Data & Model ORM (SQLAlchemy)", "Pembahasan 6 entitas tabel, foreign keys, cascade, dan property alias."),
        ("BAB III", "Skema Validasi Data (Pydantic v2)", "Pemanfaatan BaseModel, ConfigDict, dan AliasChoices dwi-bahasa."),
        ("BAB IV", "Katalog Endpoints API & Struktur Router", "Rincian 7 router (Auth, Students, Daily Reports, Assessments, Gallery, Reports, Evaluations)."),
        ("BAB V", "Layanan Khusus & Algoritma Penilaian BK", "Formula per-domain, indeks komposit, persentase, dan klasifikasi predikat perkembangan."),
        ("BAB VI", "Keamanan, Autentikasi & Otorisasi", "Bcrypt salt hashing, JWT encoding/decoding, cookie bearer, dan Role-Based Access Control."),
        ("BAB VII", "Panduan Instalasi, Konfigurasi & Eksekusi", "Persiapan env, migrasi tabel MySQL, seeding admin, dan uvicorn deployment."),
    ]
    for bab, judul, ket in daftar_isi:
        story.append(Paragraph(f"<b>{bab} — {judul}</b>", styles['SubBabTitle']))
        story.append(Paragraph(ket, styles['BodyCustom']))
        story.append(Spacer(1, 4))
    
    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── BAB I ──
    story.append(Paragraph("BAB I: ARSITEKTUR SISTEM & GAMBARAN UMUM BACKEND", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Backend pada aplikasi <b>E-Raport TK ABK</b> dibangun menggunakan bahasa pemrograman <b>Python</b> dengan framework <b>FastAPI</b>. "
        "FastAPI dipilih karena memiliki performa asinkronus yang sangat tinggi (berbasis Starlette dan Pydantic), integrasi OpenAPI otomatis (Swagger UI), "
        "serta dukungan penuh terhadap validasi tipe data statis.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>1.1 Struktur Direktori Backend</b><br/>"
        "Arsitektur kode backend dipisahkan secara modular mengikuti pola <i>Separation of Concerns (SoC)</i>:",
        styles['SubBabTitle']
    ))
    tree_backend = (
        "backend/\n"
        "├── app/\n"
        "│   ├── auth/                # Utilitas autentikasi JWT (jwt.py)\n"
        "│   ├── models/              # 6 Model ORM SQLAlchemy dalam Bahasa Indonesia\n"
        "│   │   ├── pengguna.py, siswa.py, perkembangan_harian.py\n"
        "│   │   ├── raport.py, input_penilaian.py, galeri_kegiatan.py\n"
        "│   │   └── __init__.py\n"
        "│   ├── schemas/             # 6 Skema Pydantic v2 dwi-bahasa (AliasChoices)\n"
        "│   ├── routers/             # 7 Modul router pengontrol endpoint HTTP\n"
        "│   ├── services/            # Logika bisnis & kalkulator evaluasi BK 5 domain\n"
        "│   ├── database.py          # Konfigurasi engine & sessionmaker SQLAlchemy\n"
        "│   └── main.py              # Entry point aplikasi, lifespan, SPA middleware\n"
        "└── ...\n"
        "database/\n"
        "├── schema_raport_tk.sql     # Skrip DDL MySQL terstandarisasi\n"
        "└── setup_db.py              # Skrip eksekusi migrasi & verifikasi koneksi"
    )
    story.append(Paragraph(tree_backend.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    
    story.append(Paragraph("<b>1.2 Siklus Hidup Aplikasi (Lifespan Context Manager)</b>", styles['SubBabTitle']))
    story.append(Paragraph(
        "Pada file <code>backend/app/main.py</code>, siklus startup dan shutdown dikelola secara asinkron menggunakan "
        "<code>@asynccontextmanager</code>. Saat server dinyalakan, sistem secara otomatis mengeksekusi pembuatan seluruh tabel "
        "relasional (<code>Base.metadata.create_all</code>) dan memanggil fungsi <code>seed_admin()</code> untuk memastikan "
        "akun Administrator default (<code>admin@rapor.tk</code> / <code>admin123</code>) selalu tersedia.",
        styles['BodyCustom']
    ))

    story.append(Paragraph("<b>1.3 Middleware SPA (Single Page Application) & CORS</b>", styles['SubBabTitle']))
    story.append(Paragraph(
        "Untuk memfasilitasi integrasi dengan frontend React tanpa memerlukan server Nginx tambahan saat pengujian, "
        "FastAPI dilengkapi dengan custom <code>SPAMiddleware</code>. Middleware ini memeriksa jalur permintaan; jika bukan panggilan API "
        "(seperti <code>/api</code>, <code>/students/api</code>) dan bukan aset statis (<code>/static</code>), maka permintaan dialihkan ke "
        "<code>frontend-react/dist/index.html</code>. Fitur CORS juga dibuka penuh agar client browser dapat bertukar data dengan lancar.",
        styles['BodyCustom']
    ))
    story.append(PageBreak())

    # ── BAB II ──
    story.append(Paragraph("BAB II: STRUKTUR BASIS DATA & MODEL ORM (SQLALCHEMY)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Seluruh tabel di basis data MySQL <code>raport_tk</code> dimodelkan secara terstruktur menggunakan SQLAlchemy ORM deklaratif. "
        "Penamaan tabel dan kolom basis data menggunakan Bahasa Indonesia yang konsisten, dilengkapi dengan <i>backward-compatible getters & setters</i> "
        "agar kode lama tetap dapat mengakses atribut dalam Bahasa Inggris tanpa kendala.",
        styles['BodyCustom']
    ))

    table_models = [
        [Paragraph("<b>Nama Model & Tabel</b>", styles['TableHead']), Paragraph("<b>Kolom Utama (Primary & Foreign Keys)</b>", styles['TableHead']), Paragraph("<b>Fungsi & Relasi Sistem</b>", styles['TableHead'])],
        [
            Paragraph("<b>Pengguna</b><br/>(tabel: <code>pengguna</code>)", styles['TableCellBold']),
            Paragraph("id (PK), nama, email (UNIQUE), hashed_password, peran ('admin' | 'pendamping'), tanggal_dibuat", styles['TableCell']),
            Paragraph("Menyimpan akun pengguna. Memiliki relasi satu-ke-banyak (1:N) ke siswa dampingan.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Siswa</b><br/>(tabel: <code>siswa</code>)", styles['TableCellBold']),
            Paragraph("id (PK), nama, tanggal_lahir, kebutuhan_khusus, nama_kelas, guru_id (FK -> pengguna.id)", styles['TableCell']),
            Paragraph("Biodata anak berkebutuhan khusus. Menjadi entitas induk bagi laporan, raport, galeri, dan penilaian.", styles['TableCell'])
        ],
        [
            Paragraph("<b>PerkembanganHarian</b><br/>(tabel: <code>perkembangan_harian</code>)", styles['TableCellBold']),
            Paragraph("id (PK), siswa_id (FK -> siswa.id ON DELETE CASCADE), tanggal, catatan, perilaku, interaksi_sosial", styles['TableCell']),
            Paragraph("Catatan harian perkembangan motorik, perilaku emosi, dan interaksi anak selama di sekolah.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Raport</b><br/>(tabel: <code>raport</code>)", styles['TableCellBold']),
            Paragraph("id (PK), siswa_id (FK), semester, tahun_ajaran, lingkup_perkembangan, komentar, tanggal_penilaian", styles['TableCell']),
            Paragraph("Raport kualitatif naratif semesteran anak yang siap dicetak sebagai dokumen resmi.", styles['TableCell'])
        ],
        [
            Paragraph("<b>InputPenilaian</b><br/>(tabel: <code>input_penilaian</code>)", styles['TableCellBold']),
            Paragraph("id (PK), siswa_id (FK), tanggal, kategori_usia, motorik_kasar, motorik_halus, komunikasi, sosial_emosional, kemandirian, skor_rata_rata, catatan", styles['TableCell']),
            Paragraph("Instrumen penilaian kuantitatif BK berbasis skala Likert 1-4 untuk 5 dimensi perkembangan.", styles['TableCell'])
        ],
        [
            Paragraph("<b>GaleriKegiatan</b><br/>(tabel: <code>galeri_kegiatan</code>)", styles['TableCellBold']),
            Paragraph("id (PK), siswa_id (FK), foto_url, keterangan, tanggal", styles['TableCell']),
            Paragraph("Dokumentasi foto kegiatan belajar dan terapi anak di kelas inklusi.", styles['TableCell'])
        ],
    ]
    t_models = Table(table_models, colWidths=[120, 200, 180])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2.1 Contoh Implementasi Dua Arah (Dual-Language Property Getters/Setters)</b>", styles['SubBabTitle']))
    story.append(Paragraph(
        "Teknik ini memungkinkan model SQLAlchemy diakses menggunakan nama properti Bahasa Indonesia maupun Bahasa Inggris tanpa merusak skrip lawas:",
        styles['BodyCustom']
    ))
    code_model_example = (
        "class Siswa(Base):\n"
        "    __tablename__ = 'siswa'\n"
        "    id = Column(Integer, primary_key=True, autoincrement=True)\n"
        "    nama = Column('nama', String(100), nullable=False)\n"
        "    tanggal_lahir = Column('tanggal_lahir', Date, nullable=False)\n"
        "    guru_id = Column('guru_id', Integer, ForeignKey('pengguna.id', ondelete='SET NULL'))\n"
        "\n"
        "    # Alias getter & setter untuk kompatibilitas nama properti Inggris\n"
        "    @property\n"
        "    def name(self): return self.nama\n"
        "    @name.setter\n"
        "    def name(self, val): self.nama = val\n"
        "\n"
        "    @property\n"
        "    def birth_date(self): return self.tanggal_lahir\n"
        "    @birth_date.setter\n"
        "    def birth_date(self, val): self.tanggal_lahir = val"
    )
    story.append(Paragraph(code_model_example.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(PageBreak())

    # ── BAB III ──
    story.append(Paragraph("BAB III: SKEMA VALIDASI DATA (PYDANTIC V2)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Pydantic v2 berperan sebagai garda depan validasi tipe data sebelum data masuk ke lapisan ORM database. "
        "Setiap entitas memiliki 2 jenis skema: <b>Skema Input</b> (untuk Create & Update) dan <b>Skema Respons</b> (Response).",
        styles['BodyCustom']
    ))
    story.append(Paragraph("<b>3.1 Mekanisme AliasChoices untuk Input Dwi-Bahasa</b>", styles['SubBabTitle']))
    story.append(Paragraph(
        "Fitur <code>Field(validation_alias=AliasChoices('nama', 'name'))</code> memungkinkan sistem menerima request payload JSON "
        "baik yang dikirim dengan kunci Bahasa Indonesia maupun Bahasa Inggris dari berbagai versi klien:",
        styles['BodyCustom']
    ))
    code_schema_example = (
        "class SiswaCreate(BaseModel):\n"
        "    model_config = ConfigDict(from_attributes=True, populate_by_name=True)\n"
        "    nama: str = Field(..., validation_alias=AliasChoices('nama', 'name'))\n"
        "    tanggal_lahir: datetime.date = Field(..., validation_alias=AliasChoices('tanggal_lahir', 'birth_date'))\n"
        "    kebutuhan_khusus: Optional[str] = Field(None, validation_alias=AliasChoices('kebutuhan_khusus', 'special_needs'))\n"
        "    nama_kelas: Optional[str] = Field(None, validation_alias=AliasChoices('nama_kelas', 'class_name'))\n"
        "    guru_id: Optional[int] = Field(None, validation_alias=AliasChoices('guru_id', 'teacher_id'))"
    )
    story.append(Paragraph(code_schema_example.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(Paragraph(
        "<b>Catatan Penting Python 3.14 & Pydantic v2:</b> Hindari penulisan <code>date: date</code> saat mengimpor "
        "<code>from datetime import date</code> karena akan menimbulkan tabrakan nama atribut kelas (class namespace collision). "
        "Gunakan selalu <code>import datetime</code> dan anotasi dengan <code>datetime.date</code>.",
        styles['CalloutBox']
    ))
    story.append(PageBreak())

    # ── BAB IV ──
    story.append(Paragraph("BAB IV: KATALOG ENDPOINTS API & STRUKTUR ROUTER", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Aplikasi menyediakan <b>82 rute aktif</b> yang dibagi ke dalam 7 modul router di <code>backend/app/routers/</code>:",
        styles['BodyCustom']
    ))

    routes_data = [
        [Paragraph("<b>Router File</b>", styles['TableHead']), Paragraph("<b>Endpoint Path</b>", styles['TableHead']), Paragraph("<b>Method</b>", styles['TableHead']), Paragraph("<b>Otorisasi & Deskripsi Operasi</b>", styles['TableHead'])],
        [Paragraph("auth.py", styles['TableCellBold']), Paragraph("/api/auth/login<br/>/api/auth/logout<br/>/api/auth/me<br/>/api/dashboard", styles['TableCell']), Paragraph("POST<br/>POST<br/>GET<br/>GET", styles['TableCell']), Paragraph("Autentikasi sesi JWT, verifikasi profil, serta kalkulasi ringkasan metrik dashboard.", styles['TableCell'])],
        [Paragraph("students.py", styles['TableCellBold']), Paragraph("/students/api/list<br/>/students/api/detail/{id}<br/>/students/api/add<br/>/students/api/edit/{id}<br/>/students/api/delete/{id}", styles['TableCell']), Paragraph("GET<br/>GET<br/>POST<br/>POST<br/>DELETE", styles['TableCell']), Paragraph("Manajemen data siswa. Hak Add/Edit/Delete dibatasi khusus Administrator.", styles['TableCell'])],
        [Paragraph("daily_reports.py", styles['TableCellBold']), Paragraph("/daily-reports/api/list<br/>/daily-reports/api/detail/{id}<br/>/daily-reports/api/add<br/>/daily-reports/api/edit/{id}", styles['TableCell']), Paragraph("GET<br/>GET<br/>POST<br/>POST", styles['TableCell']), Paragraph("Pencatatan perkembangan harian (aktivitas, perilaku, emosi, interaksi sosial).", styles['TableCell'])],
        [Paragraph("assessments.py", styles['TableCellBold']), Paragraph("/assessments/api/list<br/>/assessments/api/detail/{id}<br/>/assessments/api/add<br/>/assessments/api/edit/{id}", styles['TableCell']), Paragraph("GET<br/>GET<br/>POST<br/>POST", styles['TableCell']), Paragraph("Penyusunan raport capaian kualitatif semesteran siswa dampingan.", styles['TableCell'])],
        [Paragraph("evaluations.py", styles['TableCellBold']), Paragraph("/evaluations/api/add<br/>/evaluations/api/list<br/>/evaluations/api/rekap", styles['TableCell']), Paragraph("POST<br/>GET<br/>GET", styles['TableCell']), Paragraph("Instrumen observasi BK kuantitatif & rekapitulasi data komparasi grafik.", styles['TableCell'])],
        [Paragraph("gallery.py", styles['TableCellBold']), Paragraph("/gallery/api/list<br/>/gallery/api/upload<br/>/gallery/api/delete/{id}", styles['TableCell']), Paragraph("GET<br/>POST<br/>DELETE", styles['TableCell']), Paragraph("Manajemen foto kegiatan dan terapi anak.", styles['TableCell'])],
        [Paragraph("reports.py", styles['TableCellBold']), Paragraph("/reports/api/list<br/>/reports/api/detail/{student_id}", styles['TableCell']), Paragraph("GET<br/>GET", styles['TableCell']), Paragraph("Penyajian data transkrip raport lengkap siap cetak.", styles['TableCell'])],
    ]
    t_routes = Table(routes_data, colWidths=[90, 160, 50, 200])
    t_routes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_routes)
    story.append(PageBreak())

    # ── BAB V ──
    story.append(Paragraph("BAB V: LAYANAN KHUSUS & ALGORITMA PENILAIAN BK", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Modul layanan di <code>backend/app/services/evaluation_calculator.py</code> dan <code>indicators.py</code> "
        "mengimplementasikan algoritma penilaian perkembangan anak berkebutuhan khusus berbasis 5 domain esensial:",
        styles['BodyCustom']
    ))
    story.append(Paragraph("1. <b>Kognitif</b> (4 butir indikator: c1 s.d. c4)<br/>"
                           "2. <b>Motorik</b> (4 butir indikator: m1 s.d. m4)<br/>"
                           "3. <b>Bahasa & Komunikasi</b> (4 butir indikator: l1 s.d. l4)<br/>"
                           "4. <b>Sosial-Emosional</b> (4 butir indikator: s1 s.d. s4)<br/>"
                           "5. <b>Kemandirian</b> (4 butir indikator: i1 s.d. i4)", styles['BulletCustom']))
    
    story.append(Paragraph("<b>5.1 Formula Perhitungan Matematis</b>", styles['SubBabTitle']))
    story.append(Paragraph(
        "<b>a. Rata-rata Skor per Domain:</b> Dihitung dari akumulasi skor 4 indikator dibagi jumlah butir.<br/>"
        "<b>b. Indeks Komposit (Composite Index):</b> Rata-rata dari kelima domain perkembangan:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Indeks_Komposit = (Avg_Kognitif + Avg_Motorik + Avg_Bahasa + Avg_Sosial + Avg_Kemandirian) / 5</code><br/>"
        "<b>c. Persentase Indeks:</b> Normalisasi skala 1-4 ke rentang 0-100%:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Persentase = ((Indeks_Komposit - 1.0) / 3.0) * 100%</code>",
        styles['BodyCustom']
    ))
    
    story.append(Paragraph("<b>5.2 Kategori Predikat Hasil Observasi</b>", styles['SubBabTitle']))
    predikat_table = [
        [Paragraph("<b>Rentang Skor Indeks</b>", styles['TableHead']), Paragraph("<b>Kode</b>", styles['TableHead']), Paragraph("<b>Kepanjangan Predikat</b>", styles['TableHead']), Paragraph("<b>Interpretasi Klinis & Edukasi</b>", styles['TableHead'])],
        [Paragraph("3.50 — 4.00", styles['TableCellBold']), Paragraph("BSB", styles['TableCellBold']), Paragraph("Berkembang Sangat Baik", styles['TableCell']), Paragraph("Anak telah menguasai indikator secara konsisten dan mandiri tanpa bimbingan.", styles['TableCell'])],
        [Paragraph("2.50 — 3.49", styles['TableCellBold']), Paragraph("BSH", styles['TableCellBold']), Paragraph("Berkembang Sesuai Harapan", styles['TableCell']), Paragraph("Anak mampu melakukan tugas perkembangan sesuai target usia perkembangannya.", styles['TableCell'])],
        [Paragraph("1.50 — 2.49", styles['TableCellBold']), Paragraph("MB", styles['TableCellBold']), Paragraph("Mulai Berkembang", styles['TableCell']), Paragraph("Kemampuan anak mulai terlihat namun masih membutuhkan pengingat/bimbingan bertahap.", styles['TableCell'])],
        [Paragraph("1.00 — 1.49", styles['TableCellBold']), Paragraph("BB", styles['TableCellBold']), Paragraph("Belum Berkembang", styles['TableCell']), Paragraph("Anak belum menunjukkan tanda kemampuan dan memerlukan stimulasi intensif dari terapis/pendamping.", styles['TableCell'])],
    ]
    t_pred = Table(predikat_table, colWidths=[100, 50, 150, 200])
    t_pred.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_pred)
    story.append(PageBreak())

    # ── BAB VI ──
    story.append(Paragraph("BAB VI: KEAMANAN, AUTENTIKASI & OTORISASI", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Sistem menerapkan protokol keamanan berbasis standar industri untuk menjaga kerahasiaan data rekam medis dan perkembangan anak:",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>6.1 Hashing Kata Sandi dengan Bcrypt</b><br/>"
        "Kata sandi pengguna tidak pernah disimpan dalam bentuk teks polos (plain text). "
        "Fungsi <code>bcrypt.hashpw(plain.encode(), bcrypt.gensalt())</code> menyematkan salt kriptografis acak berkekuatan tinggi "
        "yang kebal terhadap serangan kamus (dictionary attack) maupun rainbow table.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>6.2 Token JWT (JSON Web Token) HS256</b><br/>"
        "Pada file <code>backend/app/auth/jwt.py</code>, token dibuat dengan masa berlaku (TTL) 8 jam (<code>ACCESS_TOKEN_EXPIRE_MINUTES = 480</code>). "
        "Klaim payload memuat <code>sub</code> (ID Pengguna), <code>name</code>, <code>email</code>, dan <code>role</code>. "
        "Token ditransmisikan secara ganda melalui <b>HTTP Cookie</b> beratribut <code>credentials: 'include'</code> serta header standar "
        "<code>Authorization: Bearer &lt;token&gt;</code>.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>6.3 Kontrol Akses Berbasis Peran (Role-Based Access Control / RBAC)</b><br/>"
        "Hak akses sistem dipisahkan tegas menjadi dua peran:",
        styles['BodyCustom']
    ))
    story.append(Paragraph("• <b>Administrator (BK / Kepala Sekolah):</b> Memiliki wewenang penuh mencakup penambahan/penghapusan siswa, manajemen pengguna dan reset PIN, pengisian evaluasi kuantitatif BK 5 domain, dan melihat rekapitulasi analitik.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Guru Pendamping (Shadow Teacher):</b> Memiliki wewenang operasional harian untuk mencatat log aktivitas belajar, perilaku & emosi, interaksi sosial, menyusun raport kualitatif naratif siswa dampingannya, serta mengunggah dokumentasi foto kegiatan.", styles['BulletCustom']))
    story.append(Spacer(1, 10))

    # ── BAB VII ──
    story.append(Paragraph("BAB VII: PANDUAN INSTALASI, KONFIGURASI & EKSEKUSI", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("<b>7.1 Persyaratan Sistem</b>", styles['SubBabTitle']))
    story.append(Paragraph("• Python 3.10 atau versi yang lebih baru.<br/>• Laragon / MySQL Server (port 3306).<br/>• Web Browser modern (Chrome / Edge / Firefox).", styles['BodyCustom']))
    
    story.append(Paragraph("<b>7.2 Langkah Menjalankan Server Backend</b>", styles['SubBabTitle']))
    code_run_backend = (
        "# 1. Pastikan MySQL di Laragon aktif\n"
        "# 2. Inisialisasi basis data (opsional jika sudah dibuat):\n"
        "python database/setup_db.py\n"
        "\n"
        "# 3. Jalankan server FastAPI dengan Uvicorn:\n"
        "uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"
    )
    story.append(Paragraph(code_run_backend.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(Paragraph(
        "Setelah server aktif, dokumentasi interaktif OpenAPI dapat diakses langsung melalui peramban web pada alamat "
        "<code>http://127.0.0.1:8000/docs</code>.",
        styles['BodyCustom']
    ))

    # Build PDF
    doc.build(story, canvasmaker=BackendNumberedCanvas)
    print(f"[OK] Selesai membuat {filename}!")


# ── FUNGSI GENERATOR PDF FRONTEND ──
def generate_frontend_pdf(filename):
    print(f"[2/2] Membuat dokumen PDF Frontend: {filename} ...")
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    styles = create_styles()
    story = []

    # ── COVER PAGE ──
    story.append(Spacer(1, 40))
    story.append(Paragraph("DOKUMENTASI TEKNIS KODE SUMBER", styles['CoverSubtitle']))
    story.append(Paragraph("SISTEM E-RAPORT TK INKLUSI ABK<br/>(FRONTEND ARCHITECTURE)", styles['CoverTitle']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="60%", thickness=2, color=colors.HexColor('#1e40af'), spaceBefore=10, spaceAfter=20))
    story.append(Paragraph("<b>Modul Analisis Arsitektur React, Vite, TypeScript Models, Manajemen State Context, Adapter API, Recharts, dan Cetak Raport</b>", styles['CoverSubtitle']))
    story.append(Spacer(1, 60))
    
    cover_table_data = [
        [Paragraph("<b>Topik Penelitian / Proyek:</b>", styles['TableCellBold']), Paragraph("Pengembangan Aplikasi Pelaporan Perkembangan Siswa TK Inklusi", styles['TableCell'])],
        [Paragraph("<b>Teknologi Inti Frontend:</b>", styles['TableCellBold']), Paragraph("React 18 (SPA), Vite 6, TypeScript 5, TailwindCSS 3", styles['TableCell'])],
        [Paragraph("<b>Visualisasi & Grafik:</b>", styles['TableCellBold']), Paragraph("Recharts (Bar Chart & Line Chart Indeks Komposit BK)", styles['TableCell'])],
        [Paragraph("<b>Standar Layout & Desain:</b>", styles['TableCellBold']), Paragraph("Golden Ratio (23.6% Sidebar : 76.4% Main Content) & CSS Print A4", styles['TableCell'])],
        [Paragraph("<b>Format Dokumen:</b>", styles['TableCellBold']), Paragraph("Buku Dokumentasi Teknis Kode Sumber Tugas Akhir (Skripsi)", styles['TableCell'])],
        [Paragraph("<b>Status Kompilasi:</b>", styles['TableCellBold']), Paragraph("Production Ready (2.634 modul ditransformasikan sukses)", styles['TableCell'])],
    ]
    t_cover = Table(cover_table_data, colWidths=[180, 310])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 70))
    story.append(Paragraph("<b>TK INKLUSI KASIH ANAK BANGSA</b><br/>Tahun Akademik 2025/2026", styles['CoverMeta']))
    story.append(PageBreak())

    # ── DAFTAR ISI ──
    story.append(Paragraph("DAFTAR ISI DOKUMENTASI FRONTEND", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=4, spaceAfter=12))
    
    daftar_isi = [
        ("BAB I", "Arsitektur Sistem & Gambaran Umum Frontend", "Teknologi React 18, Vite, TypeScript, TailwindCSS, dan filosofi desain."),
        ("BAB II", "Model & Tipe Data TypeScript (src/types/index.ts)", "Kontrak tipe entitas Bahasa Indonesia, alias dwibahasa, dan verbatimModuleSyntax."),
        ("BAB III", "Manajemen State & Konteks Global", "AuthContext (otentikasi & session sync), ToastContext (notifikasi feedback), dan PrivateRoute."),
        ("BAB IV", "Komponen Tata Letak (Layout & Navigasi)", "Struktur Layout.tsx, Sidebar.tsx (collapse & responsive mobile), dan ToastContainer."),
        ("BAB V", "Lapisan Layanan API (src/services/api.ts)", "Adapter client fetch, auto-credential bearer, dan penanganan respon REST."),
        ("BAB VI", "Pembahasan Modul & Halaman (Pages)", "Login, Dashboard (Recharts), Siswa, Laporan Harian, Raport, Penilaian BK, Galeri, dan Pengguna."),
        ("BAB VII", "Fitur Cetak Raport Formal (ReportPrint.tsx)", "Styling CSS @media print, proteksi page-break, format transkrip A4 formal 3 tanda tangan."),
        ("BAB VIII", "Panduan Build, Eksekusi & Integrasi SPA", "Perintah npm run dev, optimasi bundle produksi, dan penyajian via FastAPI SPAMiddleware."),
    ]
    for bab, judul, ket in daftar_isi:
        story.append(Paragraph(f"<b>{bab} — {judul}</b>", styles['SubBabTitle']))
        story.append(Paragraph(ket, styles['BodyCustom']))
        story.append(Spacer(1, 4))
    
    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── BAB I ──
    story.append(Paragraph("BAB I: ARSITEKTUR SISTEM & GAMBARAN UMUM FRONTEND", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Frontend aplikasi <b>E-Raport TK ABK</b> dirancang sebagai <b>Single Page Application (SPA)</b> yang modern, responsif, "
        "dan berorientasi pada kemudahan penggunaan bagi guru pendamping maupun administrator sekolah. "
        "Antarmuka mengadopsi prinsip <b>Golden Ratio (Rasio Emas)</b> untuk memastikan tata letak visual proporsional dan nyaman di mata.",
        styles['BodyCustom']
    ))
    story.append(Paragraph("<b>1.1 Struktur Direktori Frontend</b>", styles['SubBabTitle']))
    tree_frontend = (
        "frontend-react/\n"
        "├── src/\n"
        "│   ├── assets/              # Aset gambar & ilustrasi lokal\n"
        "│   ├── components/          # Komponen UI bersama (Layout, Sidebar, ToastContainer)\n"
        "│   ├── context/             # Global state (AuthContext.tsx, ToastContext.tsx)\n"
        "│   ├── pages/               # Halaman modul fungsional sistem\n"
        "│   │   ├── assessments/     # Raport kualitatif naratif\n"
        "│   │   ├── daily-reports/   # Log harian aktivitas & perilaku\n"
        "│   │   ├── evaluations/     # Observasi BK kuantitatif 5 domain & rekap komparasi\n"
        "│   │   ├── gallery/         # Galeri foto kegiatan\n"
        "│   │   ├── reports/         # Indeks & template cetak raport A4\n"
        "│   │   ├── students/        # Biodata anak berkebutuhan khusus\n"
        "│   │   ├── users/           # Manajemen pengguna & reset PIN\n"
        "│   │   ├── Dashboard.tsx    # Beranda metrik analitik & Recharts\n"
        "│   │   └── Login.tsx        # Gerbang masuk sistem\n"
        "│   ├── services/            # Client API Adapter (api.ts)\n"
        "│   ├── types/               # Tipe data TypeScript Bahasa Indonesia (index.ts)\n"
        "│   ├── App.tsx              # Router navigasi utama & proteksi hak akses\n"
        "│   └── main.tsx             # Titik render ReactDOM\n"
        "├── dist/                    # Hasil kompilasi bundel produksi\n"
        "└── package.json, vite.config.ts, tsconfig.json"
    )
    story.append(Paragraph(tree_frontend.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(PageBreak())

    # ── BAB II ──
    story.append(Paragraph("BAB II: MODEL & TIPE DATA TYPESCRIPT (SRC/TYPES/INDEX.TS)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Untuk menjamin <i>Type Safety</i> dan sinkronisasi 100% dengan backend, dibuat modul tipe data terpusat di "
        "<code>src/types/index.ts</code>. Tipe data menggunakan Bahasa Indonesia baku yang merefleksikan entitas nyata di sekolah:",
        styles['BodyCustom']
    ))

    types_table = [
        [Paragraph("<b>Interface TypeScript</b>", styles['TableHead']), Paragraph("<b>Alias Kompatibilitas</b>", styles['TableHead']), Paragraph("<b>Deskripsi Bidang & Struktur Data</b>", styles['TableHead'])],
        [Paragraph("<b>Pengguna</b>", styles['TableCellBold']), Paragraph("User, PeranPengguna", styles['TableCell']), Paragraph("id, nama, email, peran ('admin' | 'pendamping').", styles['TableCell'])],
        [Paragraph("<b>Siswa</b>", styles['TableCellBold']), Paragraph("Student", styles['TableCell']), Paragraph("id, nama, umur, tanggal_lahir, kebutuhan_khusus, nama_kelas, guru_id, nama_guru.", styles['TableCell'])],
        [Paragraph("<b>PerkembanganHarian</b>", styles['TableCellBold']), Paragraph("DailyReport, LaporanHarian", styles['TableCell']), Paragraph("id, siswa_id, nama_siswa, tanggal, catatan, perilaku, interaksi_sosial.", styles['TableCell'])],
        [Paragraph("<b>Raport</b>", styles['TableCellBold']), Paragraph("Assessment, Report", styles['TableCell']), Paragraph("id, siswa_id, semester, tahun_ajaran, lingkup_perkembangan, komentar, tanggal_penilaian.", styles['TableCell'])],
        [Paragraph("<b>InputPenilaian</b>", styles['TableCellBold']), Paragraph("Evaluation, PenilaianBK", styles['TableCell']), Paragraph("id, siswa_id, tanggal, kategori_usia, 5 domain skor (1-4), skor_rata_rata, catatan.", styles['TableCell'])],
        [Paragraph("<b>GaleriKegiatan</b>", styles['TableCellBold']), Paragraph("GalleryItem", styles['TableCell']), Paragraph("id, siswa_id, foto_url, keterangan, tanggal.", styles['TableCell'])],
        [Paragraph("<b>DataDashboard</b>", styles['TableCellBold']), Paragraph("DashboardData", styles['TableCell']), Paragraph("total_students, total_reports_today, total_assessments, recent_reports, chart_data.", styles['TableCell'])],
    ]
    t_types = Table(types_table, colWidths=[120, 130, 250])
    t_types.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_types)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Kepatuhan VerbatimModuleSyntax:</b> Dalam TypeScript konfigurasi ketat, interface/tipe diimpor menggunakan "
        "sintaks eksplisit <code>import type { Siswa, DataDashboard } from '../types';</code> sehingga kompilator "
        "Vite dapat melakukan <i>tree-shaking</i> secara optimal tanpa meninggalkan artefak JavaScript yang sia-sia.",
        styles['CalloutBox']
    ))
    story.append(PageBreak())

    # ── BAB III ──
    story.append(Paragraph("BAB III: MANAJEMEN STATE & KONTEKS GLOBAL", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "State aplikasi dikelola menggunakan <b>React Context API</b> untuk membagikan data autentikasi dan notifikasi ke seluruh hierarki komponen:",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>3.1 AuthContext (src/context/AuthContext.tsx)</b><br/>"
        "Mengelola daur hidup autentikasi pengguna. Saat aplikasi pertama kali dibuka, efek <code>useEffect</code> memanggil "
        "<code>api.checkAuth()</code> untuk memverifikasi validitas token JWT dari Cookie maupun LocalStorage. "
        "State <code>user</code> menyediakan informasi pengguna aktif (ID, nama, email, role), fungsi <code>login(email, pin)</code>, "
        "dan <code>logout()</code> yang membersihkan sesi dari peramban secara tuntas.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>3.2 ToastContext (src/context/ToastContext.tsx)</b><br/>"
        "Menyediakan sistem umpan balik instan melalui pemanggilan <code>showToast(message, type)</code>. "
        "Mendukung tipe <code>'success'</code> (hijau), <code>'error'</code> (merah), dan <code>'info'</code> (biru). "
        "Toast otomatis memudar dan menghilang setelah 3,5 detik berkat mekanisme timer asinkron.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>3.3 Komponen Pembungkus Keamanan (PrivateRoute)</b><br/>"
        "Pada file <code>src/App.tsx</code>, komponen <code>PrivateRoute</code> mengevaluasi dua lapis penjagaan:<br/>"
        "1. <b>Pemeriksaan Login:</b> Jika pengguna belum login (<code>!user</code>), dialihkan otomatis ke <code>/login</code>.<br/>"
        "2. <b>Pemeriksaan Peran (RBAC):</b> Jika pengguna tidak memiliki peran dalam prop <code>allowedRoles</code> (misal: guru pendamping mencoba mengakses <code>/users</code>), dialihkan ke <code>/dashboard</code>.",
        styles['BodyCustom']
    ))
    story.append(PageBreak())

    # ── BAB IV ──
    story.append(Paragraph("BAB IV: KOMPONEN TATA LETAK (LAYOUT & NAVIGASI)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "<b>4.1 Tata Letak Berbasis Rasio Emas (Layout.tsx)</b><br/>"
        "Membagi layar menjadi dua kolom proporsional pada desktop: Sidebar mengambil porsi <b>23.6%</b>, sementara area kerja utama mengambil porsi <b>76.4%</b>. "
        "Header navigasi atas dilengkapi dengan deteksi judul rute otomatis, penanggalan formal Bahasa Indonesia "
        "(<code>new Date().toLocaleDateString('id-ID', {...})</code>), serta badge visual peran pengguna (Administrator warna ungu, Guru Pendamping warna biru).",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>4.2 Sidebar Adaptif & Responsif (Sidebar.tsx)</b><br/>"
        "Sidebar memiliki fitur canggih yang meningkatkan kenyamanan penggunaan:",
        styles['BodyCustom']
    ))
    story.append(Paragraph("• <b>Mode Lipat Desktop (Collapse):</b> Pengguna dapat memperluas atau memperkecil sidebar melalui tombol toggle Chevron. Preferensi status tersimpan secara persisten di <code>localStorage.getItem('sidebar-collapsed')</code>.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Drawer Menu Mobile:</b> Pada layar ponsel/tablet, sidebar berubah menjadi header ringkas dengan menu drawer geser yang dibuka melalui ikon hamburger.", styles['BulletCustom']))
    story.append(Paragraph("• <b>Penyaringan Menu Berdasarkan Peran:</b> Menu 'Input Penilaian BK', 'Rekap & Komparasi', dan 'Manajemen Pengguna' hanya dirender secara kondisional jika <code>user.role === 'admin'</code>.", styles['BulletCustom']))
    story.append(PageBreak())

    # ── BAB V ──
    story.append(Paragraph("BAB V: LAPISAN LAYANAN API (SRC/SERVICES/API.TS)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Seluruh komunikasi jaringan antara aplikasi React dan server FastAPI dipusatkan pada file <code>src/services/api.ts</code>. "
        "Fungsi pembungkus <code>authFetch</code> memastikan setiap pemanggilan HTTP secara otomatis menyertakan kredensial:",
        styles['BodyCustom']
    ))
    code_fetch = (
        "async function authFetch(url: string, options: RequestInit = {}): Promise<Response> {\n"
        "  const token = localStorage.getItem('rapor_tk_token');\n"
        "  const headers = new Headers(options.headers || {});\n"
        "  if (token && !headers.has('Authorization')) {\n"
        "    headers.set('Authorization', `Bearer ${token}`);\n"
        "  }\n"
        "  return fetch(url, {\n"
        "    ...options,\n"
        "    headers,\n"
        "    credentials: 'include', // Menjamin cookie JWT selalu dikirim!\n"
        "  });\n"
        "}"
    )
    story.append(Paragraph(code_fetch.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(Paragraph(
        "Objek layanan diekspor ganda dengan nama <code>export const api = {...}</code> dan alias <code>export const apiRaport = api;</code> "
        "yang memuat metode lengkap untuk seluruh operasi CRUD sistem.",
        styles['BodyCustom']
    ))
    story.append(PageBreak())

    # ── BAB VI ──
    story.append(Paragraph("BAB VI: PEMBAHASAN MODUL & HALAMAN (PAGES)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    
    modules_data = [
        ("1. Halaman Login (Login.tsx)", "Menyediakan form autentikasi email & password/PIN. Dilengkapi efek backdrop blur glassmorphism, pencegahan submit ganda saat status loading, dan penanganan pesan error yang informatif."),
        ("2. Dashboard Utama (Dashboard.tsx)", "Menampilkan kartu statistik (total siswa, laporan hari ini, raport siap cetak), grafik batang Recharts indeks komposit per anak, grafik garis Recharts tren perkembangan bulanan, dan feed laporan harian terkini."),
        ("3. Modul Data Siswa (students/)", "• StudentList.tsx: Tabel daftar anak dengan pencarian langsung dan tautan aksi.\n• StudentForm.tsx: Form tambah/ubah profil anak dan menghubungkannya dengan guru pendamping.\n• StudentDetail.tsx: Rekam profil terpadu, rincian kebutuhan khusus, serta histori rekam harian."),
        ("4. Modul Perkembangan Harian (daily-reports/)", "• DailyReportList.tsx: Tampilan feed kronologis dengan kartu aktivitas, perilaku & emosi, interaksi sosial, serta modal pop-up detail laporan.\n• DailyReportForm.tsx: Formulir pencatatan jurnal perkembangan harian."),
        ("5. Modul Raport Kualitatif (assessments/)", "Memfasilitasi penyusunan narasi evaluasi perkembangan anak per semester. Menghasilkan deskripsi komprehensif yang menjadi komponen inti dalam raport cetak."),
        ("6. Modul Penilaian BK (evaluations/)", "• EvaluationForm.tsx: Pengisian 20 butir indikator perkembangan (skala 1-4) dengan kalkulasi skor otomatis.\n• EvaluationRekap.tsx: Visualisasi komparasi capaian siswa antar semester dalam bentuk tabel komprehensif."),
        ("7. Modul Galeri Kegiatan (gallery/)", "Menampilkan dokumentasi foto aktivitas terapi dan belajar anak dengan kemampuan filter berdasarkan siswa dan pratinjau gambar resolusi tinggi."),
        ("8. Manajemen Pengguna (users/UserList.tsx)", "Modul khusus administrator untuk mengelola akun guru pendamping, mengubah hak akses, membuat pengguna baru, dan melakukan reset PIN/kata sandi."),
    ]
    for judul, isi in modules_data:
        story.append(Paragraph(f"<b>{judul}</b>", styles['SubBabTitle']))
        story.append(Paragraph(isi.replace("\n", "<br/>"), styles['BodyCustom']))
        story.append(Spacer(1, 3))
    
    story.append(PageBreak())

    # ── BAB VII ──
    story.append(Paragraph("BAB VII: FITUR CETAK RAPORT FORMAL (REPORTPRINT.TSX)", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph(
        "Modul <code>src/pages/reports/ReportPrint.tsx</code> dirancang secara khusus untuk menghasilkan dokumen fisik "
        "buku raport resmi anak berkebutuhan khusus dengan standar percetakan kertas A4:",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>7.1 Arsitektur CSS Cetak (@media print)</b><br/>"
        "Saat tombol cetak diklik (memanggil <code>window.print()</code>), aturan CSS media print diaktifkan secara otomatis:<br/>"
        "• Seluruh elemen navigasi, tombol, dan header aplikasi disembunyikan menggunakan kelas <code>no-print</code>.<br/>"
        "• Container raport diatur menjadi lebar 100% tanpa bayangan bayang (<code>box-shadow: none !important</code>).<br/>"
        "• Menerapkan aturan <code>page-break-inside: avoid</code> pada kartu penilaian dan area tanda tangan agar tidak terpotong canggung antar halaman.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>7.2 Struktur Transkrip Raport Formal</b><br/>"
        "1. <b>Kop Surat Resmi:</b> Logo yayasan/sekolah, nama institusi, alamat, dan judul dokumen.<br/>"
        "2. <b>Tabel Biodata Siswa:</b> Nama lengkap, NIS/ID, semester, tahun ajaran, usia, dan kelas inklusi.<br/>"
        "3. <b>Tabel Capaian Kualitatif:</b> Deskripsi naratif komprehensif mengenai kemajuan belajar dan adaptasi sosial anak.<br/>"
        "4. <b>Kolom Tanda Tangan Tiga Pihak Resmi:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;a. Guru Konseling / Koordinator BK<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;b. Kepala Sekolah TK Inklusi<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;c. Guru Pendamping Khusus (Shadow Teacher)",
        styles['BodyCustom']
    ))
    story.append(Spacer(1, 8))

    # ── BAB VIII ──
    story.append(Paragraph("BAB VIII: PANDUAN BUILD, EKSEKUSI & INTEGRASI SPA", styles['BabTitle']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("<b>8.1 Perintah Pengembangan (Development Mode)</b>", styles['SubBabTitle']))
    code_dev = "cd frontend-react\nnpm run dev\n# Aplikasi aktif di http://localhost:5173"
    story.append(Paragraph(code_dev.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    
    story.append(Paragraph("<b>8.2 Perintah Kompilasi Produksi (Production Build)</b>", styles['SubBabTitle']))
    code_build = (
        "cd frontend-react\n"
        "npm run build\n"
        "# Menjalankan tsc -b (pemeriksaan tipe) disusul vite build\n"
        "# Hasil bundel terkompresi otomatis disimpan pada folder dist/"
    )
    story.append(Paragraph(code_build.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles['CodeBox']))
    story.append(Paragraph(
        "<b>8.3 Integrasi dengan FastAPI:</b> Berkat <code>SPAMiddleware</code> di backend, folder <code>dist/</code> "
        "dapat langsung disajikan oleh server FastAPI. Pengguna cukup mengakses <code>http://127.0.0.1:8000</code> untuk "
        "menggunakan seluruh aplikasi secara penuh tanpa perlu menjalankan server frontend terpisah.",
        styles['BodyCustom']
    ))

    # Build PDF
    doc.build(story, canvasmaker=FrontendNumberedCanvas)
    print(f"[OK] Selesai membuat {filename}!")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    backend_pdf_path = os.path.join(base_dir, "Dokumentasi_Backend_E_Raport_TK.pdf")
    frontend_pdf_path = os.path.join(base_dir, "Dokumentasi_Frontend_E_Raport_TK.pdf")
    
    generate_backend_pdf(backend_pdf_path)
    generate_frontend_pdf(frontend_pdf_path)
    print("\n[SUKSES] Seluruh dokumen PDF berhasil dibuat dengan sempurna!")
