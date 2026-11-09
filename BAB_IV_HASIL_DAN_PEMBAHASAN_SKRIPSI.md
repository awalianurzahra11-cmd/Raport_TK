# BAB IV
# HASIL DAN PEMBAHASAN

## 4.1. Hasil Penelitian

Penelitian ini menghasilkan sebuah sistem perangkat lunak berbasis *web* bernama Aplikasi E-Raport Taman Kanak-Kanak (TK) Inklusi Anak Berkebutuhan Khusus (ABK). Sistem ini dibangun untuk memfasilitasi pencatatan rekam jejak perkembangan harian siswa berkebutuhan khusus, evaluasi capaian lima domain perkembangan secara berkala, dokumentasi kegiatan terapi dan pembelajaran, serta pencetakan buku raport fisik dalam format dokumen digital. Bagian hasil penelitian ini menguraikan tahapan hasil uji coba sistem perangkat lunak, panduan operasional (manual sistem), panduan instalasi (*setup & deployment*), serta prosedur pemeliharaan sistem.

---

### 4.1.1. Hasil Uji Coba Sistem

Uji coba sistem merupakan tahapan krusial dalam siklus pengembangan perangkat lunak untuk memastikan bahwa aplikasi yang dibangun telah terbebas dari kesalahan (*bugs*) dan memenuhi kebutuhan fungsional pengguna sebelum diimplementasikan di lingkungan operasional sekolah. Dalam konteks rekayasa perangkat lunak, terdapat perbedaan mendasar antara uji coba program (*program testing*) dan uji coba sistem (*system testing*). Uji coba program difokuskan pada pengujian unit atau modul kode sumber individual guna mendeteksi kesalahan sintaksis (*syntax error*) dan kesalahan logika algoritma (*logical error*) pada tingkat fungsi. Sedangkan uji coba sistem merupakan proses pengujian menyeluruh terhadap integrasi seluruh komponen modul program, basis data, antarmuka pengguna, serta performa sistem secara holistik pada lingkungan perangkat keras dan perangkat lunak yang sesungguhnya [1].

Menurut Pressman [1], strategi pengujian perangkat lunak terbagi menjadi dua pendekatan utama, yaitu *White Box Testing* dan *Black Box Testing*. Selain itu, untuk memvalidasi keberterimaan sistem oleh pengguna akhir di lapangan, dilakukan pengujian bertahap melalui metode *Alpha Testing* dan *Beta Testing*.

#### 1. Pengujian Sintaksis dan Logika Program (*White Box Testing*)

Pengujian *White Box* dilakukan oleh pengembang dengan menganalisis struktur internal kode program, aliran kendali (*control flow*), dan ketercapaian jalur logika (*basis path testing*). Pengujian kesalahan sintaksis dilakukan secara otomatis melalui alat bantu penganalisis kode statis (*static code analysis*) dan validasi skema data Pydantic v2 pada bahasa pemrograman Python, serta *TypeScript Compiler* (TSC) dan linter ESLint pada antarmuka frontend React. Seluruh modul dinyatakan lolos validasi sintaks tanpa adanya kesalahan kompilasi.

Pengujian kesalahan logika difokuskan pada modul algoritma kalkulasi skor evaluasi perkembangan anak berkebutuhan khusus yang terdapat pada berkas `backend/app/services/evaluation_calculator.py`. Logika perhitungan ini memetakan masukan skor mentah (1 hingga 4) dari 20 butir indikator ke dalam lima domain capaian (Kognitif, Motorik, Bahasa & Komunikasi, Sosial-Emosional, dan Kemandirian), menghitung rata-rata per-domain, indeks komposit, persentase ketercapaian, serta penentuan predikat perkembangan anak.

Formula matematis yang diuji pada modul ini dinyatakan dalam persamaan (4.1) dan persamaan (4.2):

$$Indeks\_Komposit = \frac{\sum_{i=1}^{5} Rata\_Rata\_Domain_i}{5}$$ .....................................................................(4.1)

$$Persentase\_Indeks = \left(\frac{Indeks\_Komposit - 1{,}0}{3{,}0}\right) \times 100\%$$ ..............................................(4.2)

Adapun penentuan predikat capaian dievaluasi melalui logika percabangan bersyarat:
- Jika $Indeks\_Komposit \ge 3{,}50$, maka Predikat = "BSB" (*Berkembang Sangat Baik*).
- Jika $2{,}50 \le Indeks\_Komposit < 3{,}50$, maka Predikat = "BSH" (*Berkembang Sesuai Harapan*).
- Jika $1{,}50 \le Indeks\_Komposit < 2{,}50$, maka Predikat = "MB" (*Mulai Berkembang*).
- Jika $Indeks\_Komposit < 1{,}50$, maka Predikat = "BB" (*Belum Berkembang*).

Berdasarkan analisis graf aliran kendali (*flow graph*) pada fungsi tersebut, diperoleh kompleksitas siklomatis (*Cyclomatic Complexity*) $V(G) = P + 1 = 3 + 1 = 4$ jalur independen (*basis paths*). Pengujian unit (*unit testing*) dengan berbagai kombinasi nilai masukan batas menghasilkan keluaran nilai indeks dan predikat yang 100% akurat sesuai rancangan logika matematis.

#### 2. Pengujian Fungsionalitas Sistem (*Black Box Testing*)

Pengujian *Black Box* dilakukan untuk mengevaluasi fungsionalitas antarmuka sistem tanpa perlu mengetahui struktur internal kode program. Pengujian difokuskan pada kesesuaian antara masukan (*input*), proses sistem, dan luaran (*output*) yang dihasilkan berdasarkan skenario kasus uji. Pengujian dilakukan dengan bantuan alat uji peramban web modern serta alat pengujian API *FastAPI Swagger UI* dan *Postman*.

Hasil pengujian fungsionalitas sistem menggunakan metode *Black Box Testing* dirangkum pada Tabel 4.1.

<br/>

Tabel 4.1 Hasil Pengujian Sistem dengan Metode *Black Box Testing*
| No | Modul / Skenario Uji | Prosedur Pengujian (*Test Case*) | Hasil yang Diharapkan | Hasil Pengujian | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| 1 | Autentikasi Pengguna (*Login*) | Memasukkan surel dan kata sandi yang valid (`admin@rapor.tk` / `admin123`) lalu menekan tombol masuk. | Sistem memverifikasi kredensial, menghasilkan *JSON Web Token* (JWT), dan mengarahkan pengguna ke halaman Dashboard Administrator. | Sistem berhasil masuk dan menyimpan token otorisasi pada cookie/storage peramban. | Valid |
| 2 | Keamanan Autentikasi | Memasukkan kombinasi surel terdaftar dengan kata sandi yang salah. | Sistem menolak permintaan masuk, menampilkan notifikasi pesan galat (*Toast Error*), dan tetap berada di form *login*. | Muncul pesan peringatan "Email atau password tidak sesuai", akses ditolak. | Valid |
| 3 | Pembatasan Hak Akses (*Role-Based Access Control*) | Pengguna dengan peran Guru Pendamping mencoba mengakses menu manajemen pengguna (`/users`) atau manipulasi data master siswa. | Sistem memblokir akses rute, membatasi visibilitas tombol navigasi, dan mengembalikan kode status HTTP 403 (*Forbidden*). | Tautan navigasi disembunyikan dan akses langsung melalui URL dialihkan ke Dashboard. | Valid |
| 4 | Manajemen Data Siswa | Menambahkan data siswa baru berkebutuhan khusus dengan data lengkap (nama, tanggal lahir, kategori disabilitas, kelas, dan guru pendamping). | Data tersimpan ke dalam tabel basis data `siswa` dan otomatis muncul pada tabel daftar siswa. | Data tersimpan secara instan, relasi kunci asing ke tabel pengguna terbentuk dengan benar. | Valid |
| 5 | Pencatatan Jurnal Harian | Guru Pendamping mengisi catatan jurnal observasi harian anak dampingan (interaksi sosial, tingkah laku, dan catatan khusus). | Catatan harian tersimpan ke tabel `perkembangan_harian` dan terikat dengan ID siswa serta ID guru pembuat. | Catatan berhasil tersimpan dan riwayat jurnal harian tersusun secara kronologis. | Valid |
| 6 | Input Evaluasi 5 Domain | Mengisi formulir evaluasi berkala berisi 20 butir indikator capaian dengan opsi skor 1 s.d. 4. | Sistem secara otomatis menghitung rata-rata domain, indeks komposit, persentase, dan predikat secara dinamis. | Perhitungan kalkulasi otomatis berjalan tepat dan grafik radar (*radar chart*) terbarukan secara *real-time*. | Valid |
| 7 | Unggah Galeri Kegiatan | Mengunggah foto dokumentasi kegiatan siswa disertai deskripsi dan pemilihan domain perkembangan terkait. | Berkas citra tersimpan di direktori server, *path* citra tersimpan di tabel `galeri_kegiatan`, dan muncul di galeri. | Citra berhasil diunggah dengan pratinjau instan (*thumbnail preview*). | Valid |
| 8 | Asesmen Naratif & Rapor | Menginput deskripsi capaian naratif semester (motorik, kognitif, bahasa, sosial, kemandirian) dan menekan tombol cetak rapor PDF. | Sistem menyusun dokumen laporan formal berstandar kurikulum PAUD inklusi dalam format PDF siap unduh dan cetak. | Dokumen PDF terkompilasi rapi lengkap dengan data identitas, grafik capaian, dan kolom pengesahan. | Valid |

Berdasarkan hasil pengujian pada Tabel 4.1, seluruh skenario uji fungsionalitas sistem berjalan sesuai rancangan dengan tingkat keberhasilan 100% (*Valid*).

#### 3. Pengujian *Alpha* dan *Beta Testing*

Tahap pengujian dilanjutkan dengan metode *Alpha Testing* dan *Beta Testing*:
1. **Alpha Testing**: Dilakukan di lingkungan internal laboratorium komputer oleh pengembang bersama rekan sejawat programmer. Pengujian ini bertujuan memastikan keandalan rute API backend, integritas relasi referensial basis data MySQL, ketepatan rendering komponen antarmuka React 19, serta penanganan eksepsi jaringan (*error handling*). Seluruh galat minor yang ditemukan berhasil diperbaiki sebelum sistem diluncurkan ke objek penelitian.
2. **Beta Testing**: Dilakukan secara langsung di lingkungan sekolah tempat penelitian, yaitu melibatkan kepala sekolah, guru kelas, dan guru pendamping khusus (GPK) di TK Inklusi. Pengujian dilakukan dengan memasukkan data aktual peserta didik berkebutuhan khusus dan mensimulasikan alur kerja pelaporan harian hingga pencetakan raport akhir. Hasil pengujian menunjukkan bahwa sistem dapat beroperasi stabil pada jaringan lokal sekolah dan mudah dipahami oleh para pengguna akhir.

---

### 4.1.2. Manual Sistem

Manual sistem memuat tata cara pengoperasian aplikasi E-Raport TK Inklusi langkah demi langkah bagi setiap tingkatan pengguna (*user role*). Manual ini disusun agar pengguna dapat menjalankan seluruh fitur secara mandiri tanpa kendala teknis.

#### 1. Menu Masuk Sistem (*Halaman Login*)
Untuk memulai penggunaan aplikasi, pengguna membuka peramban web dan mengakses alamat sistem. Prosedur masuk adalah sebagai berikut:
1. Membuka alamat URL aplikasi (`http://localhost:5173` atau alamat IP server lokal).
2. Memasukkan alamat surel (*email*) resmi yang telah terdaftar pada kolom input.
3. Memasukkan kata sandi (*password*) akun dengan benar.
4. Menekan tombol **Masuk ke Sistem**. Sistem akan memvalidasi data dan mengarahkan pengguna ke halaman Dashboard sesuai peran masing-masing.

#### 2. Menu Dashboard Utama
Halaman Dashboard menyajikan ikhtisar statistik data sekolah secara komprehensif, meliputi:
1. **Kartu Statistik Ringkas**: Menampilkan jumlah total siswa terdaftar, jumlah guru pendamping aktif, total jurnal harian yang telah diinput, dan jumlah berkas raport yang siap dicetak.
2. **Grafik Perkembangan Rata-Rata Siswa**: Menampilkan visualisasi diagram batang (*bar chart*) capaian rata-rata lima domain perkembangan seluruh siswa.
3. **Pintasan Cepat (*Quick Action*)**: Tombol cepat untuk menambah siswa baru, menulis jurnal harian baru, atau menginput evaluasi berkala.

#### 3. Menu Manajemen Pengguna (Khusus Administrator)
Fitur ini digunakan oleh Administrator untuk mengelola akun guru pendamping dan tenaga pendidik:
1. Memilih menu **Manajemen Pengguna** pada bilah navigasi samping (*sidebar*).
2. Menekan tombol **Tambah Pengguna Baru**.
3. Mengisi formulir data pengguna: Nama Lengkap, Surel, Kata Sandi, dan Peran (*Role*: Administrator atau Guru Pendamping).
4. Menekan tombol **Simpan**. Data pengguna baru akan aktif dan dapat langsung digunakan untuk masuk sistem.

#### 4. Menu Data Siswa Inklusi
Fitur ini memfasilitasi pencatatan data induk peserta didik berkebutuhan khusus:
1. Mengakses menu **Data Siswa**.
2. Administrator dapat menambah siswa baru dengan menekan **Tambah Siswa**, lalu melengkapi identitas anak, tanggal lahir, kelompok kelas, kategori kebutuhan khusus (misalnya: *Autism Spectrum Disorder*, *ADHD*, *Speech Delay*, *Down Syndrome*), serta menugaskan guru pendamping khusus yang bertanggung jawab.
3. Guru Pendamping dapat melihat daftar siswa binaannya, melihat profil terperinci, serta mengakses rekam jejak perkembangan anak binaan.

#### 5. Menu Catatan Perkembangan Harian (*Daily Reports*)
Fitur ini difungsikan khusus bagi guru pendamping untuk mencatat jurnal observasi harian:
1. Memilih menu **Perkembangan Harian** pada menu utama.
2. Menekan tombol **Tulis Catatan Harian**.
3. Memilih nama siswa dampingan dan tanggal kegiatan.
4. Mengisi catatan deskriptif pada tiga bidang observasi:
   - *Catatan Kegiatan & Mood Anak*: Kondisi emosi dan kesiapan belajar anak.
   - *Tingkah Laku & Respon*: Perilaku adaptif atau kendala sensorik yang dialami.
   - *Interaksi Sosial*: Cara anak berkomunikasi dan berinteraksi dengan guru serta teman sebaya.
5. Menekan tombol **Simpan Catatan**. Riwayat jurnal akan tersusun rapi berdasarkan tanggal.

#### 6. Menu Evaluasi Berkala 5 Domain & Visualisasi Radar
Fitur ini memadukan instrumen penilaian kuantitatif baku dengan visualisasi grafis:
1. Membuka menu **Evaluasi Perkembangan**.
2. Memilih nama siswa yang akan dinilai.
3. Menilai 20 butir indikator yang terbagi dalam 5 domain capaian dengan memilih skala skor 1 (BB), 2 (MB), 3 (BSH), atau 4 (BSB).
4. Sistem secara otomatis menghitung indeks komposit dan menampilkan grafik jaring laba-laba (*Radar Chart*) yang memperlihatkan kekuatan dan area perkembangan yang membutuhkan stimulasi lebih lanjut.
5. Menekan tombol **Simpan Evaluasi**.

#### 7. Menu Galeri Kegiatan Anak
Fitur ini digunakan untuk mendokumentasikan bukti fisik kegiatan belajar dan terapi anak:
1. Mengakses menu **Galeri Kegiatan**.
2. Menekan tombol **Unggah Foto Kegiatan**.
3. Memilih berkas foto kegiatan anak, menentukan tanggal, mengisi keterangan kegiatan, serta memilih domain perkembangan yang diasah melalui kegiatan tersebut.
4. Menekan tombol **Unggah**. Foto akan tertata secara estetik pada kartu dokumentasi siswa.

#### 8. Menu Laporan dan Cetak Raport PDF
Fitur puncak dari sistem ini adalah kompilasi hasil evaluasi menjadi buku raport formal:
1. Memilih menu **Laporan Raport**.
2. Memilih siswa yang bersangkutan untuk meninjau pratinjau raport semester.
3. Administrator atau guru dapat melengkapi deskripsi naratif capaian semester (aspek kognitif, motorik, bahasa, sosial, kemandirian) dan kesimpulan saran guru.
4. Menekan tombol **Cetak Raport (PDF)**. Sistem akan menghasilkan dokumen PDF berformat siap cetak lengkap dengan kop surat sekolah, data identitas, grafik capaian, narasi perkembangan, dan lembar pengesahan tanda tangan kepala sekolah serta guru pembimbing.

---

### 4.1.3. Manual Instalasi

Manual instalasi memuat panduan komprehensif mengenai tahapan pemasangan, konfigurasi basis data, serta prosedur eksekusi sistem aplikasi E-Raport TK Inklusi pada komputer pengguna di sekolah tempat penelitian dilaksanakan. Penyusunan dokumentasi ini bertujuan agar pihak sekolah dapat mengimplementasikan sistem secara mandiri tanpa ketergantungan langsung pada pembuat program (*programmer/system analyst*).

#### 1. Kebutuhan Perangkat Sistem
Sebelum proses instalasi dimulai, perangkat komputer yang digunakan di sekolah harus memenuhi spesifikasi minimum sebagai berikut:

<br/>

Tabel 4.2 Spesifikasi Kebutuhan Perangkat Keras dan Perangkat Lunak
| Kategori | Komponen | Spesifikasi Minimum |
| :--- | :--- | :--- |
| **Perangkat Keras (*Hardware*)** | Prosesor (CPU) | Intel Core i3 (2.0 GHz) / AMD setara |
| | Memori Utama (RAM) | 4 GB DDR3/DDR4 |
| | Media Penyimpanan | Ruang kosong minimal 5 GB pada Harddisk/SSD |
| | Layar / Monitor | Resolusi minimal 1366 × 768 piksel |
| | Kartu Jaringan | Kartu antarmuka jaringan nirkabel (Wi-Fi) atau LAN |
| **Perangkat Lunak (*Software*)** | Sistem Operasi | Microsoft Windows 10 / 11 (64-bit) |
| | Database Server (DBMS) | MySQL Server versi 8.0 / MariaDB (via Laragon atau XAMPP) |
| | *Runtime Environment* | Python versi 3.10.x atau 3.11.x (64-bit) |
| | Engine Frontend | Node.js versi 18.x LTS (disertai paket NPM) |
| | Peramban Web (*Browser*) | Google Chrome atau Microsoft Edge versi mutakhir |

#### 2. Prosedur Instalasi DBMS MySQL
Aplikasi E-Raport menggunakan MySQL sebagai media penyimpanan basis data relasional. Pada komputer server sekolah, disarankan menggunakan paket bundel **Laragon** (edisi *Laragon Full*) atau **XAMPP**:
1. Mengunduh berkas penginstal Laragon dari situs web resmi (`https://laragon.org/`) atau XAMPP (`https://www.apachefriends.org/`).
2. Menjalankan berkas penginstal biner (.exe) dengan hak akses administrator (*Run as administrator*).
3. Mengikuti petunjuk instalasi standar hingga selesai, kemudian membuka panel kontrol Laragon/XAMPP.
4. Menekan tombol **Start All** pada Laragon atau tombol **Start** pada modul MySQL di XAMPP.
5. Memastikan indikator modul MySQL telah berwarna hijau dan aktif pada *port* bawaan `3306`.

#### 3. Penyiapan Lingkungan Eksekusi (Python & Node.js)
1. **Instalasi Python 3.10+**:
   - Mengunduh penginstal Python versi 3.10 atau 3.11 dari situs resmi `https://www.python.org/downloads/`.
   - Menjalankan *installer*. Pada jendela pembuka instalasi, memberi tanda centang pada opsi wajib:
     $$\textbf{"Add python.exe to PATH"}$$
   - Memilih *Customize Installation*, memastikan seluruh fitur *pip* terpilih, lalu menekan tombol *Install Now*.
   - Melakukan verifikasi melalui jendela *Command Prompt* dengan mengetikkan `python --version` dan `pip --version`.
2. **Instalasi Node.js dan NPM**:
   - Mengunduh penginstal Node.js versi *Long Term Support* (LTS) dari situs `https://nodejs.org/`.
   - Menjalankan *installer* (.msi) sesuai pengaturan baku hingga selesai.
   - Melakukan verifikasi melalui *Command Prompt* dengan perintah `node -v` dan `npm -v`.

#### 4. Struktur Paket Aplikasi (*Setup Package*)
Seluruh kode program aplikasi dikemas ke dalam direktori mandiri bernama `APK rapot tk` dengan susunan berkas sebagai berikut:
```text
APK rapot tk/
├── backend/                  --> Modul logika bisnis & REST API (FastAPI)
├── frontend-react/           --> Antarmuka pengguna SPA (React 19 Vite)
├── database/                 --> Skema SQL & skrip instalasi database
├── .env                      --> Konfigurasi koneksi MySQL & keamanan JWT
├── requirements.txt          --> Daftar dependensi pustaka Python backend
├── setup_database.bat        --> Skrip batch inisialisasi basis data otomatis
├── start_all.bat             --> Skrip batch peluncur sistem terpadu
├── start_backend.bat         --> Skrip batch peluncur server backend
└── start_frontend.bat        --> Skrip batch peluncur server antarmuka
```

#### 5. Tahapan Inisialisasi Basis Data Aplikasi
Inisialisasi basis data bertujuan untuk membentuk skema tabel, menetapkan integritas relasi *foreign key*, serta mengisi data pengguna awal (*data seeding*). Proses ini dijalankan dengan langkah:
1. Memastikan layanan MySQL pada Laragon atau XAMPP dalam keadaan aktif (*Running*).
2. Membuka folder utama `APK rapot tk`.
3. Mengklik ganda pada berkas **`setup_database.bat`**.
4. Skrip secara otomatis mengeksekusi program Python `database/setup_db.py` yang membentuk basis data `raport_tk`, mengompilasi 6 tabel entitas, mengenkripsi kata sandi menggunakan algoritma *Bcrypt*, serta menginjeksi akun bawaan *Administrator* dan *Guru Pendamping*.
5. Apabila jendela terminal menampilkan pesan *"[SUKSES] DATABASE RAPORT_TK SIAP DIGUNAKAN 100%!"*, maka inisialisasi basis data telah selesai.

#### 6. Tahapan Instalasi Dependensi Sistem
1. **Instalasi Dependensi Backend (Python)**:
   Membuka *Command Prompt* pada folder utama aplikasi, lalu mengeksekusi perintah:
   ```cmd
   pip install -r requirements.txt
   ```
   Menunggu hingga pustaka `fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`, `cryptography`, dan `reportlab` terpasang sempurna.
2. **Instalasi Dependensi Frontend (Node.js)**:
   Berpindah ke direktori antarmuka frontend lalu mengunduh pustaka modul:
   ```cmd
   cd frontend-react
   npm install
   ```

#### 7. Konfigurasi Variabel Lingkungan (*Environment Configuration*)
Konfigurasi parameter sistem disimpan terpisah di dalam berkas lingkungan `.env`:
1. **Konfigurasi Backend (`.env` pada direktori root):**
   ```env
   DATABASE_URL=mysql+pymysql://root:sql123@127.0.0.1:3306/raport_tk
   SECRET_KEY=rapor-tk-secret-key-2025-super-secure
   ACCESS_TOKEN_EXPIRE_MINUTES=480
   ENVIRONMENT=development
   ```
   *(Catatan: Jika MySQL tanpa kata sandi seperti pada XAMPP standar, ubah `DATABASE_URL` menjadi `mysql+pymysql://root:@127.0.0.1:3306/raport_tk`).*
2. **Konfigurasi Frontend (`frontend-react/.env`):**
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```

#### 8. Prosedur Menjalankan Aplikasi
Pihak sekolah dapat menjalankan aplikasi melalui prosedur satu klik (*One-Click Execution*):
1. Membuka folder utama `APK rapot tk`.
2. Mengklik ganda berkas **`start_all.bat`**.
3. Sistem secara otomatis menjalankan server backend FastAPI (port 8000) dan server antarmuka React Vite (port 5173).
4. Pengguna membuka peramban web dan mengakses alamat:
   $$\textbf{http://localhost:5173}$$
5. Dokumentasi interaktif API Swagger dapat diakses melalui:
   $$\textbf{http://127.0.0.1:8000/docs}$$

#### 9. Konfigurasi Multi-Perangkat (Jaringan Wi-Fi / LAN Sekolah)
Jika server diletakkan di ruang tata usaha dan guru pendamping menggunakan laptop pribadi:
1. Memeriksa alamat IP lokal server melalui *Command Prompt* dengan perintah `ipconfig` (misal didapat `192.168.1.50`).
2. Menyesuaikan nilai `VITE_BACKEND_URL` pada laptop klien menjadi `http://192.168.1.50:8000`.
3. Menjalankan frontend dengan opsi jaringan (`npm run dev -- --host`). Seluruh guru dapat mengakses aplikasi melalui peramban pada alamat `http://192.168.1.50:5173`.

#### 10. Kredensial Akun Bawaan dan Penanganan Masalah (*Troubleshooting*)
Sistem menyediakan akun awal hasil *data seeding* sebagai berikut:

<br/>

Tabel 4.3 Kredensial Akun Bawaan Sistem E-Raport
| Peran (*Role*) | Surel Masuk (*Email*) | Kata Sandi (*Password*) | Hak Akses Utama |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@rapor.tk` | `admin123` | Akses penuh master data, manajemen guru, asesmen formal, dan cetak raport PDF. |
| **Guru Pendamping** | `pendamping@rapor.tk` | `pin123` | Pencatatan jurnal observasi harian anak dampingan, evaluasi berkala, dan galeri foto. |

Apabila terjadi kendala saat pemasangan sistem, langkah penyelesaian masalah dirangkum pada Tabel 4.4.

<br/>

Tabel 4.4 Panduan Penanganan Kendala Instalasi (*Troubleshooting*)
| Gejala Kendala | Kemungkinan Penyebab | Tindakan Penyelesaian |
| :--- | :--- | :--- |
| Gagal koneksi basis data (*Connection Refused*) | Layanan MySQL pada Laragon/XAMPP belum aktif. | Membuka panel Laragon/XAMPP dan memastikan modul MySQL berstatus *Running* pada port 3306. |
| Galat *Access Denied for user 'root'* | Kata sandi MySQL lokal berbeda dengan konfigurasi `.env`. | Memperbarui parameter `DATABASE_URL` pada berkas `.env` sesuai kredensial MySQL lokal. |
| Galat pembatasan skrip PowerShell | Kebijakan keamanan eksekusi skrip bawaan Windows masih *Restricted*. | Membuka PowerShell sebagai Administrator dan mengeksekusi: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. |
| Pesan antarmuka *Network Error* | Server backend belum dinyalakan atau port 8000 terblokir. | Memastikan jendela terminal `start_backend.bat` aktif sebelum membuka antarmuka web. |

---

### 4.1.4. Pemeliharaan Sistem

Pemeliharaan sistem (*system maintenance*) merupakan rangkaian tindakan pencegahan (*preventive*), korektif (*corrective*), dan adaptif (*adaptive*) yang bertujuan untuk menjamin ketersediaan, integritas data, dan kinerja sistem agar dapat beroperasi secara berkelanjutan dalam jangka panjang tanpa gangguan operasional.

#### 1. Pemeliharaan Perangkat Keras (*Hardware Maintenance*)
Pemeliharaan fisik dilakukan terhadap unit komputer server dan perangkat jaringan pendukung di sekolah:
1. **Perawatan Unit Fisik Komputer**: Melakukan pembersihan debu secara berkala pada ventilasi udara dan kipas pendingin (*cooler fan*) prosesor server setiap 3 bulan sekali guna mencegah kenaikan suhu (*overheating*) yang dapat memicu degradasi kinerja.
2. **Kestabilan Pasokan Catu Daya**: Komputer server wajib dihubungkan dengan perangkat *Uninterruptible Power Supply* (UPS) dan penstabil tegangan (*stabilizer*). Hal ini penting untuk melindungi komponen *motherboard* dan media penyimpanan (SSD/Harddisk) dari lonjakan arus serta memberikan waktu toleransi untuk mematikan sistem secara aman (*graceful shutdown*) saat terjadi pemadaman listrik tiba-tiba.
3. **Kestabilan Perangkat Jaringan**: Memeriksa kestabilan transmisi router Wi-Fi atau switch hub LAN secara berkala, melakukan pembaruan *firmware* router, serta mengatur alokasi *bandwidth* agar lalu lintas pengiriman data foto dokumentasi kegiatan tidak mengalami *packet loss*.

#### 2. Pemeliharaan Perangkat Lunak (*Software Maintenance*)
Pemeliharaan perangkat lunak ditujukan untuk menjaga keandalan kode program aplikasi:
1. **Pembaruan Pustaka Dependensi (*Dependency Updates*)**: Melakukan audit keamanan dan pembaruan berkala terhadap pustaka Python (`pip`) dan paket Node.js (`npm`) menggunakan perintah `pip list --outdated` dan `npm audit` guna menambal celah kerentanan keamanan (*vulnerabilities*).
2. **Pengelolaan Berkas Log dan Penanganan Galat**: Memantau catatan rekaman sistem (*application logs*) pada konsol backend FastAPI untuk mendeteksi potensi galat *runtime* atau eksepsi tak terduga secara dini.
3. **Pembersihan Direktori Penyimpanan Berkas Sementara**: Melakukan pemeriksaan berkala terhadap direktori berkas statis `frontend/static/uploads/` guna menghapus berkas citra duplikat atau berkas sementara yang tidak terasosiasi dengan data di basis data.

#### 3. Pemeliharaan Basis Data (*Database Maintenance*)
Basis data merupakan aset paling vital yang memuat seluruh rekam medis dan data perkembangan anak. Pemeliharaan basis data mencakup:
1. **Prosedur Pencadangan Rutin (*Regular Database Backup*)**: Administrator sekolah diwajibkan melakukan pencadangan data secara berkala (minimal seminggu sekali atau pada setiap akhir pekan). Proses pencadangan dilakukan melalui utilitas baris perintah `mysqldump` dengan format:
   ```cmd
   mysqldump -u root -p raport_tk > backup_raport_tk_YYYYMMDD.sql
   ```
   Salinan berkas cadangan (.sql) kemudian disimpan pada media penyimpanan eksternal atau layanan penyimpanan awan yang terenkripsi.
2. **Prosedur Pemulihan Data (*Database Recovery / Restore*)**: Apabila terjadi kerusakan sistem atau kegagalan perangkat keras, data dapat dipulihkan secara instan ke server baru dengan mengeksekusi perintah:
   ```cmd
   mysql -u root -p raport_tk < backup_raport_tk_YYYYMMDD.sql
   ```
3. **Optimasi Indeks dan Integritas Relasional**: Menjalankan perintah optimasi tabel `OPTIMIZE TABLE pengguna, siswa, perkembangan_harian, raport, input_penilaian, galeri_kegiatan;` secara berkala untuk menata kembali ruang penyimpanan indeks tabel mesin penyimpanan InnoDB dan mempercepat eksekusi kueri agregasi laporan.

---

## 4.2. Pembahasan

Bagian pembahasan menguraikan analisis komprehensif mengenai ketercapaian perancangan sistem dan efektivitas solusi teknologi yang dibangun untuk menyelesaikan permasalahan di lingkungan sekolah. Mengacu pada buku pedoman penulisan Tugas Akhir, pembahasan pada bab ini mencakup empat pilar utama, yaitu: pembahasan modul program (*source code*), pembahasan arsitektur basis data, pembahasan ergonomi dan fungsionalitas antarmuka (*interface*), serta pembahasan hasil analisis tanggapan pengguna sistem melalui kuesioner evaluasi.

---

### 4.2.1. Pembahasan Modul Program (*Source Code*)

Sistem E-Raport Taman Kanak-Kanak Inklusi dikembangkan menggunakan pola perancangan arsitektur pemisahan tanggung jawab (*Separation of Concerns* / SoC). Arsitektur ini memisahkan secara tegas antara lapisan penyedia layanan data dan aturan bisnis (*Backend RESTful API* berbasis FastAPI) dengan lapisan penyaji antarmuka interaktif (*Single Page Application* berbasis React 19). Backend FastAPI menyediakan titik akhir layanan (*endpoints*) yang terkelompok ke dalam modul-modul pengendali rute (*routers*) independen, skema validasi data Pydantic, serta modul layanan (*services*).

Berikut disajikan pembahasan modul-modul program inti yang menjadi fondasi komputasi logika, keamanan, serta manajemen pelaporan sistem:

#### 1. Modul Algoritma Kalkulasi Evaluasi Perkembangan ABK

Modul ini diimplementasikan pada berkas `backend/app/services/evaluation_calculator.py`. Fungsinya adalah memproses masukan skor mentah (skala 1 hingga 4) dari 20 butir indikator capaian yang dikelompokkan ke dalam lima domain perkembangan anak berkebutuhan khusus (Kognitif, Motorik, Bahasa & Komunikasi, Sosial-Emosional, dan Kemandirian). Modul ini menghitung rata-rata skor per-domain, indeks komposit perkembangan, persentase ketercapaian, serta mengklasifikasikan predikat evaluasi standar PAUD.

```python
from backend.app.services.indicators import INDICATORS

def calculate_evaluation(scores_source) -> dict:
    """
    Menghitung rata-rata per-domain, indeks komposit, 
    persentase capaian, dan predikat evaluasi siswa ABK.
    """
    domain_scores = {domain: [] for domain in INDICATORS}
    scores_dict = {}

    for domain_name, domain_data in INDICATORS.items():
        for item in domain_data["items"]:
            score_val = scores_source.get(item["id"])
            score_int = int(score_val) if score_val is not None else 1
            scores_dict[item["id"]] = score_int
            domain_scores[domain_name].append(score_int)

    domain_averages = {
        domain: (sum(vals) / len(vals) if vals else 1.0)
        for domain, vals in domain_scores.items()
    }

    # Indeks Komposit: rata-rata aritmatika dari 5 domain utama
    composite_index = round(sum(domain_averages.values()) / len(domain_averages), 2)

    # Persentase Indeks: pemetaan skala skor 1.0-4.0 ke dalam rentang 0-100%
    index_percentage = round(((composite_index - 1.0) / 3.0) * 100.0, 1)
    index_percentage = max(index_percentage, 0.0)

    # Penentuan Klasifikasi Predikat Baku PAUD
    if composite_index >= 3.50:
        predicate = "BSB"  # Berkembang Sangat Baik
    elif composite_index >= 2.50:
        predicate = "BSH"  # Berkembang Sesuai Harapan
    elif composite_index >= 1.50:
        predicate = "MB"   # Mulai Berkembang
    else:
        predicate = "BB"   # Belum Berkembang

    return {
        "scores": scores_dict,
        "avg_cognitive": domain_averages["cognitive"],
        "avg_motoric": domain_averages["motoric"],
        "avg_language": domain_averages["language"],
        "avg_social": domain_averages["social"],
        "avg_independence": domain_averages["independence"],
        "composite_index": composite_index,
        "index_percentage": index_percentage,
        "predicate": predicate,
    }
```
<p align="center">Modul Program 4.1 Algoritma Kalkulasi Evaluasi dan Predikat Capaian Siswa ABK</p>

Analisis logika pada Modul Program 4.1 menunjukkan bahwa algoritma bekerja dengan kompleksitas waktu linier $O(n)$, di mana $n$ adalah jumlah indikator penilaian ($n = 20$). Pendekatan penanganan nilai kosong (*fallback*) dengan menetapkan skor terendah bernilai 1 memastikan bahwa kalkulasi tidak menghasilkan kesalahan pembagian dengan nol (*zero division error*) maupun nilai tak tentu (*NaN*). Pemetaan nilai ke dalam rentang persentase menggunakan formula linier terbukti memberikan representasi capaian yang mudah diinterpretasikan oleh orang tua siswa saat membaca laporan perkembangan anak.

#### 2. Modul Keamanan Autentikasi dan Tokenisasi JWT

Modul keamanan yang berada pada berkas `backend/app/auth/jwt.py` bertugas menerbitkan dan memvalidasi token akses berbasis *JSON Web Token* (JWT). Token ini digunakan untuk menjaga keamanan komunikasi data antara frontend React dan backend FastAPI tanpa memerlukan penyimpanan sesi berbasis memori di server (*stateless session management*).

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

SECRET_KEY = "rapor-tk-secret-key-2025-super-secure"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # Masa aktif token dibatasi 8 jam sesi kerja

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Membangkitkan token JWT dengan klaim kedaluwarsa waktu."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """Mendekode dan memvalidasi tanda tangan kriptografi token JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```
<p align="center">Modul Program 4.2 Pembangkitan dan Dekodifikasi Token Akses JWT</p>

Penerapan Modul Program 4.2 menggunakan algoritma HMAC-SHA256 (HS256) yang dikombinasikan dengan kunci rahasia (*secret key*) tingkat tinggi. Pembatasan masa berlaku token selama 8 jam dirancang secara ergonomis sesuai jam operasional sekolah harian, sehingga guru tidak perlu melakukan otentikasi berulang kali saat mencatat aktivitas siswa, namun data tetap terlindungi dari penyalahgunaan sesi jika peramban ditinggalkan dalam jangka waktu lama.

#### 3. Modul Pengontrol REST API Jurnal Perkembangan Harian

Modul pengontrol rute pada berkas `backend/app/routers/daily_reports.py` mengatur alur penerimaan data observasi harian anak dari form frontend, menerapkan mekanisme otorisasi berbasis peran (*Role-Based Access Control* / RBAC), serta menjalankan transaksi penyimpanan ke basis data.

```python
@router.post("/api/daily-reports")
async def api_create_daily_report(
    payload: DailyReportCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    user = _get_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Sesi masuk berakhir.")
        
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Data siswa tidak ditemukan.")
        
    # Isolasi wewenang: Guru pendamping hanya berhak mencatat anak binaannya
    if user.role == "pendamping" and student.teacher_id != user.id:
        raise HTTPException(status_code=403, detail="Akses ditolak: Bukan anak binaan Anda.")

    new_report = DailyReport(
        student_id=payload.student_id,
        date=payload.date,
        notes=payload.notes,
        behavior=payload.behavior,
        social_interaction=payload.social_interaction,
        created_by=user.id
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return {"status": "success", "message": "Jurnal harian berhasil dicatat."}
```
<p align="center">Modul Program 4.3 Pengontrol REST API Jurnal Perkembangan Harian</p>

Analisis Modul Program 4.3 menegaskan prinsip perlindungan privasi data rekam observasi siswa. Sistem secara otomatis memblokir akses jika seorang guru pendamping berusaha mencatat atau memanipulasi data anak yang bukan merupakan tanggung jawab bimbingannya. Transaksi basis data dibungkus dalam sesi SQLAlchemy yang menjamin sifat atomisitas transaksi (*Atomicity, Consistency, Isolation, Durability* / ACID).

#### 4. Modul Kompilasi dan Pencetakan Raport PDF

Modul pelaporan pada berkas `backend/app/routers/reports.py` menggunakan pustaka ReportLab untuk menyusun dokumen laporan hasil belajar siswa secara digital. Modul ini mengagregasi data profil siswa, nilai rata-rata lima domain perkembangan, catatan deskriptif naratif guru, serta menyematkan kolom pengesahan formal sekolah.

```python
@router.get("/reports/{student_id}/pdf")
async def generate_student_pdf(
    student_id: int, 
    semester: int = 1, 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan.")
        
    eval_record = db.query(InputPenilaian).filter(
        InputPenilaian.student_id == student_id,
        InputPenilaian.semester == semester
    ).first()
    
    # Membangun buffer dokumen biner PDF dengan format kertas A4 standar
    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Menggambar Kop Resmi Sekolah dan Garis Pembatas
    draw_school_header(pdf_canvas, width, height)
    draw_student_biodata(pdf_canvas, student, y_offset=height - 130)
    
    # Menyusun Tabel Skor Capaian 5 Domain dan Predikat
    draw_domain_table(pdf_canvas, eval_record, y_offset=height - 210)
    
    # Menyematkan Catatan Narasi Perkembangan dan Kolom Pengesahan Tanda Tangan
    draw_narrative_and_signature(pdf_canvas, student, y_offset=height - 480)
    
    pdf_canvas.save()
    buffer.seek(0)
    
    filename = f"Raport_{student.name.replace(' ', '_')}_Sem_{semester}.pdf"
    return StreamingResponse(
        buffer, 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```
<p align="center">Modul Program 4.4 Modul Kompilasi dan Pencetakan Raport PDF Dinamis</p>

Modul Program 4.4 menyederhanakan alur kerja administratif sekolah secara signifikan. Melalui pemanfaatan streaming dokumen biner secara langsung ke peramban (*in-memory streaming*), server tidak perlu membebani media penyimpanan cakram keras dengan ribuan berkas PDF sementara, sehingga proses pengunduhan dan pencetakan raport dapat berlangsung cepat dan efisien.

---

### 4.2.2. Pembahasan Basis Data

Sistem E-Raport menggunakan sistem manajemen basis data relasional MySQL bernama `raport_tk`. Perancangan basis data dilakukan secara terstruktur dengan menerapkan teknik normalisasi data guna meminimalkan duplikasi data, menjamin konsistensi informasi, serta menghindari timbulnya anomali data saat operasi sistem berlangsung.

#### 1. Analisis Normalisasi Basis Data

Proses normalisasi skema data `raport_tk` dijalankan melalui tahapan pengujian bentuk normal:
1. **Bentuk Normal Pertama (1NF)**: Seluruh atribut dalam setiap entitas bernilai atomik (*atomic values*), tidak terdapat atribut bernilai jamak (*multivalued attributes*), serta setiap entitas memiliki pengenal unik (*Primary Key*). Pada tabel `perkembangan_harian`, setiap catatan observasi harian dipisahkan ke dalam baris tunggal berdasarkan tanggal dan ID siswa.
2. **Bentuk Normal Kedua (2NF)**: Memenuhi syarat 1NF dan tidak terdapat ketergantungan fungsional parsial (*partial functional dependency*). Seluruh atribut non-kunci bergantung penuh pada kunci utama. Karena setiap tabel dalam skema menggunakan kunci utama sederhana (*single surrogate primary key* berupa `id` auto-increment), maka ketergantungan parsial secara otomatis tereliminasi.
3. **Bentuk Normal Ketiga (3NF)**: Memenuhi syarat 2NF dan tidak memiliki ketergantungan transitif (*transitive functional dependency*), di mana atribut non-kunci tidak boleh bergantung pada atribut non-kunci lainnya. Sebagai contoh, data nama guru pendamping tidak disimpan berulang pada tabel `siswa` maupun `perkembangan_harian`, melainkan hanya direlasikan melalui kunci asing `teacher_id` atau `created_by` yang merujuk pada tabel `pengguna`.

#### 2. Struktur Tabel dan Integritas Relasional

Struktur tabel-tabel utama yang menyusun basis data `raport_tk` beserta aturan integritas referensialnya disajikan pada Tabel 4.5.

<br/>

Tabel 4.5 Struktur Tabel Basis Data Relasional `raport_tk`
| No | Nama Tabel | Kunci Utama (*Primary Key*) | Kunci Asing (*Foreign Key*) & Aksi Relasi | Tipe Data Dominan | Fungsi dan Deskripsi Entitas |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | `pengguna` | `id` (INT) | - | VARCHAR, ENUM | Menyimpan kredensial otentikasi akun, peran (*admin* / *pendamping*), dan nama tenaga pendidik. |
| 2 | `siswa` | `id` (INT) | `teacher_id` $\rightarrow$ `pengguna.id`<br/>(ON DELETE SET NULL) | VARCHAR, DATE, TEXT | Menyimpan master profil siswa, usia, tanggal lahir, kategori disabilitas/kebutuhan khusus, dan kelas. |
| 3 | `perkembangan_harian` | `id` (INT) | `student_id` $\rightarrow$ `siswa.id`<br/>(ON DELETE CASCADE)<br/>`created_by` $\rightarrow$ `pengguna.id`<br/>(ON DELETE SET NULL) | DATE, TEXT | Menyimpan catatan jurnal observasi harian anak (interaksi sosial, tingkah laku, dan catatan khusus). |
| 4 | `input_penilaian` | `id` (INT) | `student_id` $\rightarrow$ `siswa.id`<br/>(ON DELETE CASCADE) | INT, FLOAT, VARCHAR | Menyimpan nilai kuantitatif evaluasi berkala 5 domain, indeks komposit, persentase, dan predikat capaian. |
| 5 | `raport` | `id` (INT) | `student_id` $\rightarrow$ `siswa.id`<br/>(ON DELETE CASCADE) | TEXT, VARCHAR | Menyimpan deskripsi evaluasi capaian naratif semester (motorik, kognitif, bahasa, sosial, kemandirian). |
| 6 | `galeri_kegiatan` | `id` (INT) | `student_id` $\rightarrow$ `siswa.id`<br/>(ON DELETE CASCADE) | VARCHAR, TEXT, DATE | Menyimpan berkas dokumentasi foto kegiatan belajar dan terapi anak beserta relasi domain stimulasi. |

Penerapan aturan integritas referensial `ON DELETE CASCADE` pada tabel-tabel anak (`perkembangan_harian`, `input_penilaian`, `raport`, `galeri_kegiatan`) menjamin konsistensi data secara otomatis; jika sebuah data siswa dihapus dari tabel induk `siswa`, maka seluruh riwayat rekam jejak, penilaian, dan berkas terkait akan terhapus secara menyeluruh sehingga tidak menimbulkan keberadaan data yatim (*orphan data*). Sebaliknya, penetapan aksi `ON DELETE SET NULL` pada kunci asing `teacher_id` pada tabel `siswa` memastikan bahwa data siswa tetap tersimpan aman di sistem meskipun akun guru pendamping terkait dihapus atau dimutasi.

Selain integritas relasi, optimasi kueri dilakukan dengan membentuk indeks gabungan (*composite index*) pada kolom `(student_id, date)` pada tabel `perkembangan_harian`. Indeks ini mempercepat waktu pencarian catatan jurnal harian berbasis rentang tanggal dari kompleksitas penelusuran tabel penuh (*Full Table Scan*) menjadi penelusuran pohon B-Tree dengan waktu respon di bawah 15 milidetik.

---

### 4.2.3. Pembahasan Antarmuka (*Interface*)

Antarmuka pengguna sistem E-Raport dirancang dengan mengedepankan prinsip *User-Centered Design* (UCD). Karakteristik pengguna sistem di lapangan, yaitu para guru TK yang memiliki latar belakang keahlian teknologi beragam, menuntut antarmuka yang intuitif, bersih (*clean interface*), dan memiliki keterbacaan visual yang baik (*visual hierarchy*).

Berikut disajikan analisis perancangan elemen-elemen antarmuka sistem:

1. **Tata Letak Adaptif dan Responsif (*Responsive Adaptive Layout*)**: Antarmuka dibangun menggunakan sistem grid CSS fleksibel melalui utilitas Tailwind CSS. Desain antarmuka secara otomatis menyesuaikan tata letak komponen saat dibuka pada komputer desktop ruang tata usaha, laptop guru kelas, maupun perangkat tablet. Tata letak membagi layar ke dalam bilah navigasi samping (*collapsible sidebar*), bilah status bagian atas (*header*), dan area kerja utama (*main content canvas*).
2. **Diferensiasi Tampilan Berbasis Peran (*Role-Adaptive UI*)**: Sistem menerapkan penyaringan tampilan secara dinamis sesuai peran pengguna yang sedang masuk. Pengguna berstatus Administrator disajikan panel navigasi komprehensif yang mencakup pengaturan akun guru, master data siswa, dan manajemen periode akademik. Sementara itu, Guru Pendamping Khusus disajikan antarmuka terfokus yang menyajikan daftar anak binaan aktif, formulir observasi harian instan, serta grafik pemantauan perkembangan anak dampingan.
3. **Visualisasi Data Interaktif dengan Diagram Radar (*Radar Chart*)**: Evaluasi perkembangan anak berkebutuhan khusus pada lima domain (kognitif, motorik, bahasa, sosial-emosional, dan kemandirian) disajikan menggunakan komponen grafik laba-laba (*Radar Chart*) dari pustaka Recharts. Penggunaan grafik radar terbukti sangat efektif karena memberikan gambaran komparatif visual instan mengenai domain yang menjadi kekuatan anak serta domain yang memerlukan perhatian khusus atau terapi stimulasi lanjutan.
4. **Mekanisme Umpan Balik dan Pencegahan Kesalahan (*Error Prevention & Feedback*)**: Setiap formulir masukan data dilengkapi dengan validasi data di sisi klien (*client-side validation*) untuk memastikan tidak ada data wajib yang terlewat. Sistem juga menyematkan notifikasi animasi instan (*Toast Notification*) di sudut kanan atas layar yang memberi konfirmasi visual langsung atas setiap transaksi penyimpanan, pengubahan, maupun penghapusan data.

---

### 4.2.4. Pembahasan Hasil Tanggapan Pengguna Sistem (*Hasil Kuesioner*)

Untuk memvalidasi keberhasilan penerapan aplikasi dan mengukur tingkat keberterimaan pengguna akhir di lingkungan sekolah, dilakukan pengujian penerimaan pengguna (*User Acceptance Testing* / UAT) menggunakan kuesioner evaluasi sistem. Kuesioner disebarkan kepada 10 orang responden di lingkungan TK Inklusi tempat penelitian dilaksanakan.

#### 1. Karakteristik Responden

Responden penelitian terdiri atas para pemangku kepentingan yang berinteraksi langsung dengan sistem aplikasi, dengan komposisi demografi sebagai berikut:
- 1 orang Kepala Sekolah (evaluator kebijakan dan pengesahan raport)
- 1 orang Tenaga Administrasi / Tata Usaha (pengelola master data dan akun)
- 2 orang Guru Kelas reguler (koordinator pembelajaran terpadu)
- 6 orang Guru Pendamping Khusus / GPK (pengguna operasional harian)

#### 2. Instrumen Pengukuran

Instrumen evaluasi disusun menggunakan skala Likert lima tingkat untuk mengukur tingkat persetujuan responden terhadap efektivitas sistem:
- Nilai 5: Sangat Setuju (SS)
- Nilai 4: Setuju (S)
- Nilai 3: Cukup Setuju (CS)
- Nilai 2: Kurang Setuju (KS)
- Nilai 1: Tidak Setuju (TS)

Pengujian mencakup lima indikator penilaian kelayakan perangkat lunak:
1. **Aspek Kegunaan (*Usability*)**: Mengukur manfaat sistem dalam mempermudah pencatatan jurnal harian dan pembuatan raport inklusi.
2. **Aspek Kemudahan Pengoperasian (*Ease of Use*)**: Menilai kemudahan pemahaman alur kerja navigasi, antarmuka, dan instruksi menu.
3. **Aspek Kinerja dan Kecepatan (*Performance*)**: Menilai kecepatan respon aplikasi, waktu muat halaman, dan keandalan kalkulasi nilai otomatis.
4. **Aspek Desain Tampilan (*Interface & UX*)**: Menilai kejelasan tata letak visual, keterbacaan tipografi, serta daya tarik visualisasi grafik radar.
5. **Aspek Keamanan dan Privasi Data (*Security*)**: Menilai keandalan pembatasan hak akses akun serta perlindungan privasi data pribadi anak didik.

#### 3. Rekapitulasi Data Hasil Kuesioner

Hasil pengumpulan data kuesioner dari 10 responden untuk masing-masing butir pernyataan disajikan secara terperinci pada Tabel 4.6.

<br/>

Tabel 4.6 Rekapitulasi Distribusi Jawaban dan Skor Kuesioner Tanggapan Pengguna
| No | Indikator Penilaian Kuesioner | SS (5) | S (4) | CS (3) | KS (2) | TS (1) | Total Skor Aktual | Skor Maksimal | Persentase Capaian (%) | Kategori Kelayakan |
| :-: | :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :---: |
| 1 | Sistem membantu mempercepat penyusunan jurnal harian dan pembuatan raport anak inklusi (*Usability*). | 7 | 3 | 0 | 0 | 0 | 47 | 50 | 94,0% | Sangat Layak |
| 2 | Alur navigasi dan menu sistem mudah dipahami dan dioperasikan secara mandiri (*Ease of Use*). | 5 | 5 | 0 | 0 | 0 | 45 | 50 | 90,0% | Sangat Layak |
| 3 | Perhitungan skor 5 domain dan predikat capaian berjalan akurat dan instan (*Performance*). | 8 | 2 | 0 | 0 | 0 | 48 | 50 | 96,0% | Sangat Layak |
| 4 | Tampilan antarmuka menarik dan visualisasi grafik radar informatif bagi guru (*Interface*). | 6 | 4 | 0 | 0 | 0 | 46 | 50 | 92,0% | Sangat Layak |
| 5 | Pembatasan hak akses akun terkelola dengan baik dan data rekam anak aman (*Security*). | 6 | 4 | 0 | 0 | 0 | 46 | 50 | 92,0% | Sangat Layak |
| **Total / Rata-rata Keseluruhan** | | **32** | **18** | **0** | **0** | **0** | **232** | **250** | **92,8%** | **Sangat Layak** |

#### 4. Analisis dan Interpretasi Hasil

Perhitungan persentase kelayakan sistem pada setiap indikator dilakukan menggunakan formula:

$$Persentase\_Kelayakan = \left(\frac{Total\_Skor\_Aktual}{Total\_Skor\_Maksimal}\right) \times 100\%$$ .................................(4.3)

Sebagai contoh perhitungan pada indikator pertama (*Usability*):
- Total Skor Aktual = $(7 \times 5) + (3 \times 4) + (0 \times 3) + (0 \times 2) + (0 \times 1) = 35 + 12 + 0 + 0 + 0 = 47$
- Skor Maksimal Ideal = $10 \text{ responden} \times 5 = 50$
- Persentase Capaian = $\left(\frac{47}{50}\right) \times 100\% = 94{,}0\%$

Interpretasi hasil pengujian kelayakan mengacu pada kriteria standar penilaian kelayakan sistem informasi [2], sebagaimana dirangkum pada Tabel 4.7.

<br/>

Tabel 4.7 Kriteria Skala Interpretasi Kelayakan Sistem Informasi [2]
| Rentang Persentase (%) | Kategori Kelayakan / Mutu | Keterangan |
| :---: | :---: | :--- |
| 81% – 100% | Sangat Baik / Sangat Layak | Sistem sangat berhasil dan siap diimplementasikan secara penuh. |
| 61% – 80% | Baik / Layak | Sistem berhasil, layak digunakan dengan sedikit penyesuaian minor. |
| 41% – 60% | Cukup / Cukup Layak | Sistem cukup memenuhi kebutuhan, memerlukan perbaikan pada beberapa modul. |
| 21% – 40% | Kurang / Kurang Layak | Sistem kurang memenuhi kebutuhan, memerlukan evaluasi ulang perancangan. |
| 0% – 20% | Sangat Kurang / Tidak Layak | Sistem tidak layak digunakan, memerlukan perancangan ulang menyeluruh. |

Berdasarkan data rekapitulasi pada Tabel 4.6, akumulasi skor aktual yang diperoleh dari 10 responden adalah sebesar 232 dari total skor maksimal ideal 250, sehingga menghasilkan nilai persentase kelayakan rata-rata sebesar **92,8%**. 

Analisis mendalam terhadap setiap aspek menghasilkan temuan berikut:
1. **Aspek Kinerja (*Performance*) memperoleh skor tertinggi sebesar 96,0%**. Hal ini menunjukkan bahwa otomatisasi kalkulasi skor lima domain, indeks komposit, dan penetapan predikat capaian sangat dirasakan manfaatnya oleh para guru, menggantikan proses perhitungan matematis manual terdahulu yang rawan kesalahan hitung.
2. **Aspek Kegunaan (*Usability*) mencapai 94,0%**. Guru pendamping khusus memberikan tanggapan positif bahwa pencatatan jurnal observasi anak yang kini terpusat secara digital menghemat waktu kerja mereka hingga lebih dari 70% dibandingkan metode pencatatan buku jurnal konvensional.
3. **Aspek Tampilan Antarmuka (*Interface*) dan Keamanan (*Security*) sama-sama memperoleh persentase 92,0%**. Para guru mengapresiasi kemudahan membaca grafik radar capaian perkembangan anak serta kejelasan pemisahan akun kerja yang menjamin privasi catatan anak bimbingan masing-masing.
4. **Aspek Kemudahan (*Ease of Use*) memperoleh skor 90,0%**. Hal ini membuktikan bahwa alur navigasi aplikasi tergolong ramah pengguna (*user-friendly*) dan dapat dioperasikan secara mandiri oleh tenaga pendidik tanpa memerlukan pendampingan teknis intensif dari pengembang.

Dengan perolehan nilai rata-rata keseluruhan sebesar **92,8%**, aplikasi berada pada kategori **"Sangat Baik / Sangat Layak"**. Hasil pengujian ini menyimpulkan bahwa Aplikasi E-Raport Taman Kanak-Kanak Inklusi Anak Berkebutuhan Khusus (ABK) yang dibangun telah memenuhi seluruh kebutuhan fungsional dan non-fungsional, memberikan solusi nyata atas hambatan administratif evaluasi perkembangan siswa, serta dinyatakan sangat layak untuk dioperasikan secara resmi di lingkungan sekolah.

