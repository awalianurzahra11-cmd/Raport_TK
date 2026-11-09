# DOKUMEN MANUAL INSTALASI SISTEM
**Berdasarkan Pedoman Penulisan Tugas Akhir STITEK Bontang (Versi Revisi 2021 - Poin 7.1.3 Manual Instalasi)**

---

## 4.1.3. Manual Instalasi
Manual instalasi memuat panduan komprehensif mengenai tahapan pemasangan dan konfigurasi sistem aplikasi E-Raport Taman Kanak-Kanak (TK) Inklusi Anak Berkebutuhan Khusus (ABK) pada komputer pengguna/sekolah tempat penelitian dilaksanakan. Penyusunan manual ini bertujuan agar pihak sekolah (administrator sekolah maupun guru pendamping) dapat melakukan proses instalasi dan implementasi sistem secara mandiri tanpa ketergantungan langsung pada pengembang sistem (*programmer/system analyst*).

---

### 1. Kebutuhan Perangkat Sistem
Sebelum proses instalasi dimulai, perangkat komputer yang akan digunakan di sekolah harus memenuhi spesifikasi kebutuhan minimum sebagai berikut:

Tabel 4.1 Spesifikasi Kebutuhan Perangkat Keras dan Perangkat Lunak
| Kategori | Komponen | Spesifikasi Minimum |
| :--- | :--- | :--- |
| **Perangkat Keras** | Prosesor (CPU) | Intel Core i3 (2.0 GHz) / AMD setara |
| | Memori (RAM) | 4 GB DDR3/DDR4 |
| | Media Penyimpanan | Ruang kosong minimal 5 GB pada Harddisk/SSD |
| | Layar / Monitor | Resolusi minimal 1366 × 768 piksel |
| | Jaringan | Kartu antarmuka jaringan (Wi-Fi / LAN) |
| **Perangkat Lunak** | Sistem Operasi | Microsoft Windows 10 / 11 (64-bit) |
| | Database Server | MySQL Server versi 8.0 atau MariaDB (via Laragon / XAMPP) |
| | Python Runtime | Python versi 3.10.x atau 3.11.x (64-bit) |
| | Node.js Engine | Node.js versi 18.x LTS (disertai paket NPM) |
| | Web Browser | Google Chrome / Microsoft Edge versi terkini |

---

### 2. Prosedur Instalasi DBMS (Database Management System) MySQL
Aplikasi E-Raport TK Inklusi menggunakan MySQL sebagai sistem manajemen basis data relasional. Pada lingkungan sekolah, disarankan menggunakan bundel perangkat lunak **Laragon** atau **XAMPP** untuk mempermudah operasional.

Tahapan instalasi dan konfigurasi DBMS adalah sebagai berikut:
1. Mengunduh berkas penginstal Laragon (disarankan edisi *Laragon Full*) melalui situs web resmi (`https://laragon.org/download/`) atau XAMPP (`https://www.apachefriends.org/`).
2. Menjalankan berkas instalasi *installer* (.exe) dengan hak akses administrator (*Run as administrator*).
3. Mengikuti instruksi instalasi standar hingga selesai, lalu menjalankan aplikasi Laragon/XAMPP.
4. Menekan tombol **Start All** pada panel Laragon atau tombol **Start** pada modul MySQL di XAMPP.
5. Memastikan indikator layanan MySQL telah berwarna hijau dan berjalan pada *port* bawaan `3306`.

---

### 3. Persiapan Lingkungan Eksekusi (Python & Node.js)
Sistem E-Raport dibangun menggunakan backend Python FastAPI dan antarmuka React Vite. Pihak sekolah perlu memastikan lingkungan *runtime* telah dipasang pada komputer server:

#### a. Instalasi Python 3.10+
1. Mengunduh berkas penginstal Python versi 3.10 atau 3.11 dari situs resmi `https://www.python.org/downloads/windows/`.
2. Menjalankan *installer*. Pada jendela pertama instalasi, memberi tanda centang pada opsi:
   $$\textbf{"Add python.exe to PATH"}$$
   *(Langkah ini sangat krusial agar perintah python dapat dipanggil melalui terminal).*
3. Menekan opsi **Customize Installation**, memastikan seluruh fitur *pip*, *IDLE*, dan *py launcher* terpilih, kemudian mengklik tombol **Install Now**.
4. Melakukan verifikasi melalui Command Prompt dengan mengetikkan perintah `python --version` dan `pip --version`.

#### b. Instalasi Node.js dan NPM
1. Mengunduh berkas instalasi Node.js versi Long Term Support (LTS) dari situs `https://nodejs.org/`.
2. Melakukan instalasi berkas biner (.msi) sesuai dengan pengaturan standar (*default*).
3. Melakukan verifikasi keberhasilan instalasi melalui Command Prompt dengan perintah `node -v` dan `npm -v`.

---

### 4. Proses Pembuatan Paket Aplikasi (*Packaging / Setup Package*)
Seluruh kode sumber, aset visual, skrip inisialisasi basis data, serta pustaka pendukung dikemas ke dalam satu direktori paket mandiri bernama `APK rapot tk`. Struktur paket aplikasi yang diserahkan ke pihak sekolah meliputi:

```text
APK rapot tk/
├── backend/                  --> Modul pemroses logika bisnis & API (FastAPI)
├── frontend-react/           --> Antarmuka pengguna berbasis SPA (React Vite)
├── database/                 --> Berkas migrasi & skema SQL (schema_raport_tk.sql, setup_db.py)
├── .env                      --> Berkas konfigurasi koneksi database & JWT Secret
├── requirements.txt          --> Daftar dependensi pustaka Python backend
├── setup_database.bat        --> Skrip otomatis inisialisasi basis data
├── start_all.bat             --> Skrip peluncur sistem terpadu (Dual-Runner)
├── start_backend.bat         --> Skrip peluncur khusus server backend
└── start_frontend.bat        --> Skrip peluncur khusus antarmuka web
```

---

### 5. Tahapan Instalasi Basis Data Aplikasi
Inisialisasi basis data bertujuan untuk membentuk skema tabel, menetapkan relasi *foreign key*, serta mengisi data pengguna awal (*data seeding*). Proses ini telah diotomatisasi melalui berkas eksekusi batch:

1. Memastikan layanan MySQL pada Laragon / XAMPP telah dalam keadaan aktif (*Running*).
2. Membuka folder utama `APK rapot tk`.
3. Mengklik ganda pada berkas **`setup_database.bat`**.
4. Skrip secara otomatis mengeksekusi program Python `database/setup_db.py` yang melakukan operasi:
   - Membuat basis data `raport_tk` dengan set karakter `utf8mb4`.
   - Mengompilasi seluruh tabel entitas: `pengguna`, `siswa`, `daily_reports`, `evaluations`, `rekap_evaluasi`, `galeri_kegiatan`, dan `assessments`.
   - Melakukan *hashing* kata sandi menggunakan pustaka `bcrypt`.
   - Menginjeksi akun bawaan *Administrator* dan *Guru Pendamping*.
5. Apabila pada jendela terminal menampilkan pesan *"[SUKSES] Setup database selesai 100%!"*, maka inisialisasi basis data telah selesai.

```sql
CREATE DATABASE IF NOT EXISTS `raport_tk` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
*Modul Program 4.1 Potongan Perintah Pembuatan Basis Data MySQL*

---

### 6. Tahapan Instalasi Dependensi Sistem
Sebelum aplikasi dapat dijalankan untuk pertama kali, dependensi pustaka backend dan frontend harus diunduh dan dipasang:

#### a. Instalasi Dependensi Backend (FastAPI)
1. Membuka terminal Command Prompt dan mengarahkan ke direktori utama aplikasi:
   ```cmd
   cd "C:\Users\USER\Documents\Tugas Akhir\APK rapot tk"
   ```
2. Menjalankan perintah instalasi pustaka Python:
   ```cmd
   pip install -r requirements.txt
   ```
3. Menunggu hingga seluruh pustaka (`fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`, `cryptography`, `reportlab`, dll.) terpasang secara sempurna.

#### b. Instalasi Dependensi Frontend (React.js)
1. Berpindah ke subdirektori antarmuka frontend:
   ```cmd
   cd frontend-react
   ```
2. Menjalankan perintah pengunduhan paket antarmuka:
   ```cmd
   npm install
   ```
3. Menunggu hingga folder `node_modules` terbentuk dan seluruh paket dependensi UI selesai terpasang.

---

### 7. Konfigurasi Variabel Lingkungan (*Environment Configuration*)
Konfigurasi parameter sistem disimpan terpisah di dalam berkas lingkungan `.env` agar memudahkan penyesuaian tanpa mengubah kode program:

1. **Konfigurasi Server Backend (`.env` pada direktori root):**
   ```env
   DATABASE_URL=mysql+pymysql://root:sql123@127.0.0.1:3306/raport_tk
   SECRET_KEY=rapor-tk-secret-key-2025-super-secure
   ACCESS_TOKEN_EXPIRE_MINUTES=480
   ENVIRONMENT=development
   ```
   *Catatan:* Apabila kata sandi MySQL pada komputer pengguna dikosongkan (bawaan XAMPP), maka nilai `DATABASE_URL` disesuaikan menjadi:
   `mysql+pymysql://root:@127.0.0.1:3306/raport_tk`.

2. **Konfigurasi Antarmuka Klien (`frontend-react/.env`):**
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```

---

### 8. Prosedur Menjalankan Aplikasi (*System Execution*)
Proses eksekusi aplikasi dirancang fleksibel untuk memudahkan pengoperasian harian oleh pihak sekolah:

#### a. Eksekusi Sekali Klik (*One-Click Dual Execution*)
1. Membuka folder utama `APK rapot tk`.
2. Mengklik ganda pada berkas **`start_all.bat`**.
3. Sistem secara otomatis menjalankan server backend (FastAPI pada port 8000) dan server frontend (Vite React pada port 5173).
4. Pengguna dapat membuka peramban web dan mengakses alamat:
   $$\textbf{http://localhost:5173}$$

#### b. Eksekusi Terpisah (*Independent Service*)
Apabila ingin memantau log sistem secara terperinci, aplikasi dapat dijalankan secara terpisah:
- **Server Backend:** Mengklik ganda berkas `start_backend.bat` (aktif pada `http://127.0.0.1:8000`). Dokumentasi pengujian API Swagger dapat diakses pada `http://127.0.0.1:8000/docs`.
- **Server Frontend:** Mengklik ganda berkas `start_frontend.bat` (aktif pada `http://localhost:5173`).

---

### 9. Konfigurasi Penggunaan Multi-Perangkat (Jaringan LAN / Wi-Fi Sekolah)
Apabila komputer server diletakkan di ruang tata usaha/kepala sekolah, dan para guru pendamping menggunakan laptop pribadi melalui jaringan Wi-Fi sekolah:

1. Mengetahui alamat IP lokal komputer server dengan membuka Command Prompt dan mengetikkan perintah `ipconfig`. Mencatat alamat IPv4 (misalnya: `192.168.1.50`).
2. Mengubah nilai konfigurasi pada berkas `frontend-react/.env` pada perangkat klien menjadi:
   ```env
   VITE_BACKEND_URL=http://192.168.1.50:8000
   ```
3. Menjalankan frontend dengan opsi jaringan (`npm run dev -- --host`).
4. Perangkat guru dapat mengakses aplikasi melalui peramban dengan memasukkan URL `http://192.168.1.50:5173`.

---

### 10. Verifikasi Keberhasilan Instalasi dan Akun Pengguna Awal
Keberhasilan proses instalasi dapat diverifikasi dengan melakukan *login* ke dalam sistem menggunakan akun bawaan hasil *seeding* basis data:

Tabel 4.2 Kredensial Akun Bawaan Sistem E-Raport TK Inklusi
| Peran Pengguna (*Role*) | Surel Masuk (*Email*) | Kata Sandi / PIN | Hak Akses Utama |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@rapor.tk` | `admin123` | Master data siswa, manajemen akun pengguna, asesmen BK, rekap penilaian, cetak raport formal. |
| **Guru Pendamping** | `pendamping@rapor.tk` | `pin123` | Pencatatan jurnal aktivitas harian anak dampingan, penilaian naratif semester, galeri foto dokumentasi. |

---

### 11. Penanganan Kendala Instalasi (*Troubleshooting*)
Apabila ditemukan kendala selama proses instalasi, tindakan perbaikan dapat dilakukan berdasarkan panduan berikut:

Tabel 4.3 Panduan Pemecahan Masalah Instalasi
| Gejala Permasalahan | Kemungkinan Penyebab | Tindakan Penyelesaian |
| :--- | :--- | :--- |
| Gagal koneksi ke MySQL (*Connection Refused*) | Layanan MySQL pada Laragon/XAMPP belum dijalankan atau *port 3306* terblokir. | Membuka panel kontrol Laragon/XAMPP dan memastikan modul MySQL telah berstatus *Running*. Memeriksa apakah terdapat instans MySQL lain di `services.msc`. |
| Kesalahan otentikasi MySQL (*Access Denied for user 'root'*) | Kata sandi pada berkas `.env` berbeda dengan konfigurasi MySQL lokal pengguna. | Menyesuaikan berkas `.env` pada parameter `DATABASE_URL` sesuai kata sandi MySQL komputer yang digunakan. |
| Kesalahan eksekusi skrip PowerShell (*Running Scripts is Disabled*) | Pembatasan kebijakan keamanan eksekusi skrip bawaan Windows. | Membuka Windows PowerShell dengan hak Administrator, lalu mengeksekusi perintah: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. |
| Tampilan antarmuka menampilkan pesan *Network Error* | Server backend FastAPI belum aktif atau URL backend pada `frontend-react/.env` tidak sesuai. | Memastikan berkas `start_backend.bat` telah dijalankan dan memeriksa alamat URL yang dituju pada berkas konfigurasi frontend. |
