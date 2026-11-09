/**
 * Model & Tipe Data TypeScript E-Raport TK (Bahasa Indonesia)
 * Mendukung dual-naming / alias bahasa Inggris untuk kompatibilitas penuh.
 */

// ── 1. PENGGUNA (USER) ──
export type PeranPengguna = 'admin' | 'pendamping';

export interface Pengguna {
  id: number;
  nama: string;
  email: string;
  peran: PeranPengguna;
  // Properti alias backward-compatibility
  name?: string;
  role?: PeranPengguna;
}

export type User = Pengguna;

// ── 2. SISWA (STUDENT) ──
export interface Siswa {
  id: number;
  nama: string;
  umur?: number;
  tanggal_lahir: string;
  kebutuhan_khusus?: string;
  nama_kelas?: string;
  guru_id?: number;
  nama_guru?: string;
  // Properti alias backward-compatibility
  name?: string;
  age?: number;
  birth_date?: string;
  special_needs?: string;
  class_name?: string;
  teacher_id?: number;
  teacher_name?: string;
}

export type Student = Siswa;

// ── 3. PERKEMBANGAN HARIAN (DAILY REPORT) ──
export interface PerkembanganHarian {
  id: number;
  siswa_id: number;
  nama_siswa?: string;
  tanggal: string;
  catatan?: string;
  perilaku?: string;
  interaksi_sosial?: string;
  // Properti alias backward-compatibility
  student_id?: number;
  student_name?: string;
  date?: string;
  report_date?: string;
  notes?: string;
  behavior?: string;
  social_interaction?: string;
}

export type DailyReport = PerkembanganHarian;
export type LaporanHarian = PerkembanganHarian;

// ── 4. RAPORT KUALITATIF (RAPORT / ASSESSMENT) ──
export interface Raport {
  id: number;
  siswa_id: number;
  nama_siswa?: string;
  semester: number;
  tahun_ajaran: string;
  lingkup_perkembangan?: string;
  komentar?: string;
  tanggal_penilaian?: string;
  // Properti alias backward-compatibility
  student_id?: number;
  student_name?: string;
  academic_year?: string;
  development_domain?: string;
  comments?: string;
  assessment_date?: string;
}

export type Assessment = Raport;
export type Report = Raport;
export type RaportKualitatif = Raport;

// ── 5. INPUT PENILAIAN BK (EVALUATION) ──
export interface InputPenilaian {
  id: number;
  siswa_id: number;
  nama_siswa?: string;
  tanggal: string;
  kategori_usia?: string;
  // 5 Dimensi Penilaian
  motorik_kasar?: number;
  motorik_halus?: number;
  komunikasi?: number;
  sosial_emosional?: number;
  kemandirian?: number;
  skor_rata_rata?: number;
  catatan?: string;
  // Properti alias backward-compatibility
  student_id?: number;
  student_name?: string;
  evaluation_date?: string;
  age_group?: string;
  gross_motor?: number;
  fine_motor?: number;
  communication?: number;
  social_emotional?: number;
  independence?: number;
  average_score?: number;
  notes?: string;
}

export type Evaluation = InputPenilaian;
export type PenilaianBK = InputPenilaian;

// ── 6. GALERI KEGIATAN (GALLERY ITEM) ──
export interface GaleriKegiatan {
  id: number;
  siswa_id: number;
  nama_siswa?: string;
  foto_url: string;
  keterangan?: string;
  tanggal?: string;
  // Properti alias backward-compatibility
  student_id?: number;
  student_name?: string;
  image_url?: string;
  photo_url?: string;
  caption?: string;
  date?: string;
  activity_date?: string;
}

export type GalleryItem = GaleriKegiatan;

// ── 7. DASHBOARD DATA ──
export interface DataDashboard {
  total_students: number;
  total_reports_today: number;
  total_assessments: number;
  total_gallery_items: number;
  total_graded_students: number;
  recent_reports: PerkembanganHarian[];
  chart_data: {
    bar: {
      labels: string[];
      data: number[];
    };
    line: {
      labels: string[];
      data: number[];
    };
  };
}

export type DashboardData = DataDashboard;
