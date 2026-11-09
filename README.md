# 📚 PANDUAN LENGKAP INSTALASI & MENJALANKAN SISTEM E-RAPORT TK ABK
**Paket Standalone: Backend-Fix (FastAPI) + Frontend-React (Modern UI)**

---

## 📋 DAFTAR ISI
1. [Prasyarat Perangkat Lunak](#1-prasyarat-perangkat-lunak)
2. [Langkah 1: Setup Database MySQL](#2-langkah-1-setup-database-mysql)
3. [Langkah 2: Instalasi Dependensi Backend (Python)](#3-langkah-2-instalasi-dependensi-backend-python)
4. [Langkah 3: Instalasi Dependensi Frontend (Node.js React)](#4-langkah-3-instalasi-dependensi-frontend-nodejs-react)
5. [Langkah 4: Menjalankan Aplikasi](#5-langkah-4-menjalankan-aplikasi)
6. [Langkah 5: Konfigurasi Multi-Device (Jaringan Wi-Fi/LAN)](#6-langkah-5-konfigurasi-multi-device-jaringan-wi-filan)
7. [Informasi Akun Bawaan (Default Login)](#7-informasi-akun-bawaan-default-login)

---

## 1. Prasyarat Perangkat Lunak
Pastikan perangkat komputer telah terpasang:
- **Python 3.10+** (Centang *"Add python.exe to PATH"* saat instalasi).
- **Node.js 18+ & NPM** (Download di [nodejs.org](https://nodejs.org/)).
- **Laragon / XAMPP** (Untuk menjalankan MySQL Server di Port 3306).

---

## 2. Langkah 1: Setup Database MySQL

1. Buka **Laragon** atau **XAMPP**, klik tombol **Start All** (pastikan MySQL di port 3306 aktif).
2. Anda memiliki 2 cara untuk membuat database:
   - **Cara A (Otomatis dengan 1 Klik):**
     Klik ganda file `setup_database.bat` di folder utama.
   - **Cara B (Manual via Terminal):**
     ```bash
     python database/setup_db.py
     ```
   - **Cara C (Import via HeidiSQL / phpMyAdmin):**
     Buka phpMyAdmin (`http://localhost/phpmyadmin`) atau HeidiSQL, lalu import file `database/schema_raport_tk.sql`.

*Database `raport_tk` beserta tabel dan akun default akan otomatis terbuat 100%!*

---

## 3. Langkah 2: Instalasi Dependensi Backend (Python)

Buka Terminal / Command Prompt pada folder utama paket ini, lalu jalankan:
```bash
pip install -r requirements.txt
```

---

## 4. Langkah 3: Instalasi Dependensi Frontend (Node.js React)

Masuk ke folder `frontend-react` lalu install dependensinya:
```bash
cd frontend-react
npm install
cd ..
```

---

## 5. Langkah 4: Menjalankan Aplikasi

### Pilihan 1: Jalankan Sekaligus (*Paling Praktis*)
Cukup klik ganda file:
👉 **`start_all.bat`** (atau jalankan `python run_dev.py` di terminal).

Browser dapat dibuka di:
- **Frontend React:** `http://localhost:5173`
- **Backend FastAPI:** `http://127.0.0.1:8000`
- **Dokumentasi Swagger API:** `http://127.0.0.1:8000/docs`

### Pilihan 2: Jalankan Terpisah
- **Terminal 1 (Backend):** Jalankan `start_backend.bat` atau `python run_backend.py`
- **Terminal 2 (Frontend React):** Jalankan `start_frontend.bat` atau masuk ke `cd frontend-react && npm run dev`

---

## 6. Langkah 5: Konfigurasi Multi-Device (Jaringan Wi-Fi/LAN)

Jika Backend berada di **Komputer A (Server)** dan Guru mengakses dari **Laptop B (Klien)**:

1. **Di Komputer A (Server):**
   - Cek IP Server di CMD: `ipconfig` (misal didapat `192.168.1.50`).
   - Jalankan `start_backend.bat`.
2. **Di Laptop B (Klien):**
   - Buka file `frontend-react/.env`.
   - Ubah baris `VITE_BACKEND_URL` menjadi:
     ```env
     VITE_BACKEND_URL=http://192.168.1.50:8000
     ```
   - Jalankan `npm run dev` di folder `frontend-react`.
   - Buka browser di Laptop B: `http://localhost:5173`.

---

## 7. Informasi Akun Bawaan (Default Login)

| Role Pengguna | Email Login | Password / PIN | Hak Akses |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@rapor.tk` | `admin123` | Master Siswa, Manajemen User, Penilaian BK, Rekap Evaluasi, Cetak Raport PDF |
| **Guru Pendamping** | `pendamping@rapor.tk` | `pin123` | Catatan Harian Siswa Dampingan, Penilaian Naratif, Galeri Foto Dokumentasi |
