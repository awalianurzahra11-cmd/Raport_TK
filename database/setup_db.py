import pymysql
import bcrypt
import sys

def hash_pw(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def setup():
    print("=" * 60)
    print("  SETUP DATABASE MYSQL UNTUK RAPOR TK ABK")
    print("=" * 60)
    
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = "sql123" # Password default di database.py
    
    try:
        # Coba koneksi dengan password sql123
        conn = pymysql.connect(host=host, port=port, user=user, password=password)
    except Exception:
        try:
            # Fallback jika root tanpa password
            print("[INFO] Mencoba login MySQL root tanpa password...")
            conn = pymysql.connect(host=host, port=port, user=user, password="")
            password = ""
        except Exception as e:
            print(f"[ERROR] Gagal terhubung ke MySQL: {e}")
            print("Pastikan MySQL di Laragon / XAMPP sudah dinyalakan (Port 3306).")
            sys.exit(1)
            
    cursor = conn.cursor()
    print("[1/3] Membuat database 'raport_tk'...")
    cursor.execute("CREATE DATABASE IF NOT EXISTS `raport_tk` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute("USE `raport_tk`;")
    
    print("[2/3] Membuat tabel-tabel sistem...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `pengguna` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(100) NOT NULL,
        `email` VARCHAR(150) NOT NULL UNIQUE,
        `hashed_password` VARCHAR(255) NOT NULL,
        `role` ENUM('admin', 'pendamping') NOT NULL DEFAULT 'pendamping'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `siswa` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `name` VARCHAR(150) NOT NULL,
        `age` INT DEFAULT 0,
        `birth_date` VARCHAR(50) NULL,
        `special_needs` VARCHAR(255) NULL,
        `class_name` VARCHAR(50) NULL,
        `teacher_id` INT NULL,
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`teacher_id`) REFERENCES `pengguna`(`id`) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `perkembangan_harian` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `student_id` INT NOT NULL,
        `date` DATE NOT NULL,
        `notes` TEXT NULL,
        `behavior` TEXT NULL,
        `social_interaction` TEXT NULL,
        `created_by` INT NULL,
        FOREIGN KEY (`student_id`) REFERENCES `siswa`(`id`) ON DELETE CASCADE,
        FOREIGN KEY (`created_by`) REFERENCES `pengguna`(`id`) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `raport` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `student_id` INT NOT NULL,
        `period` VARCHAR(50) NOT NULL,
        `motoric` TEXT NULL,
        `language` TEXT NULL,
        `social` TEXT NULL,
        `cognitive` TEXT NULL,
        `independence` TEXT NULL,
        `summary` TEXT NULL,
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`student_id`) REFERENCES `siswa`(`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `input_penilaian` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `student_id` INT NOT NULL,
        `date` DATE NOT NULL,
        `class_name` VARCHAR(50) NULL,
        `diagnosa` VARCHAR(255) NULL,
        `scores` TEXT NULL,
        `avg_cognitive` FLOAT DEFAULT 0,
        `avg_motoric` FLOAT DEFAULT 0,
        `avg_language` FLOAT DEFAULT 0,
        `avg_social` FLOAT DEFAULT 0,
        `avg_independence` FLOAT DEFAULT 0,
        `composite_index` FLOAT DEFAULT 0,
        `index_percentage` FLOAT DEFAULT 0,
        `predicate` VARCHAR(10) DEFAULT 'BB',
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`student_id`) REFERENCES `siswa`(`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS `galeri_kegiatan` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `student_id` INT NOT NULL,
        `image_path` VARCHAR(500) NOT NULL,
        `description` TEXT NULL,
        `domain` VARCHAR(100) NULL,
        `date` DATE NOT NULL,
        FOREIGN KEY (`student_id`) REFERENCES `siswa`(`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')
    
    print("[3/3] Memeriksa akun bawaan (Admin & Pendamping)...")
    cursor.execute("SELECT id FROM pengguna WHERE email = 'admin@rapor.tk';")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO pengguna (name, email, hashed_password, role) VALUES (%s, %s, %s, %s);",
            ("Administrator", "admin@rapor.tk", hash_pw("admin123"), "admin")
        )
        print("  [+] Akun Admin dibuat: admin@rapor.tk / admin123")
        
    cursor.execute("SELECT id FROM pengguna WHERE email = 'pendamping@rapor.tk';")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO pengguna (name, email, hashed_password, role) VALUES (%s, %s, %s, %s);",
            ("Guru Pendamping", "pendamping@rapor.tk", hash_pw("pin123"), "pendamping")
        )
        print("  [+] Akun Pendamping dibuat: pendamping@rapor.tk / pin123")
        
    conn.commit()
    conn.close()
    print("=" * 60)
    print(" [SUKSES] DATABASE RAPORT_TK SIAP DIGUNAKAN 100%!")
    print("=" * 60)

if __name__ == "__main__":
    setup()
