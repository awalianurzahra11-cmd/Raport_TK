-- ====================================================================
-- SKEMA DATABASE: raport_tk
-- SISTEM E-RAPORT TK ANAK BERKEBUTUHAN KHUSUS (ABK)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `raport_tk` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `raport_tk`;

-- 1. TABEL PENGGUNA (AKUN SISTEM)
CREATE TABLE IF NOT EXISTS `pengguna` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(150) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `role` ENUM('admin', 'pendamping') NOT NULL DEFAULT 'pendamping'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. TABEL SISWA (DATA ANAK DIDIK)
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

-- 3. TABEL PERKEMBANGAN_HARIAN (CATATAN HARIAN)
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

-- 4. TABEL RAPORT (PENILAIAN NARATIF/KUALITATIF)
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

-- 5. TABEL INPUT_PENILAIAN (PENILAIAN KUANTITATIF BK)
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

-- 6. TABEL GALERI_KEGIATAN (FOTO KEGIATAN DOKUMENTASI)
CREATE TABLE IF NOT EXISTS `galeri_kegiatan` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `student_id` INT NOT NULL,
    `image_path` VARCHAR(500) NOT NULL,
    `description` TEXT NULL,
    `domain` VARCHAR(100) NULL,
    `date` DATE NOT NULL,
    FOREIGN KEY (`student_id`) REFERENCES `siswa`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. DEFAULT USER DATA (ADMIN & PENDAMPING)
-- Default Password admin: admin123
-- Default Password pendamping: pin123
INSERT INTO `pengguna` (`name`, `email`, `hashed_password`, `role`)
SELECT 'Administrator', 'admin@rapor.tk', '$2b$12$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'admin'
WHERE NOT EXISTS (SELECT 1 FROM `pengguna` WHERE `email` = 'admin@rapor.tk');

INSERT INTO `pengguna` (`name`, `email`, `hashed_password`, `role`)
SELECT 'Guru Pendamping', 'pendamping@rapor.tk', '$2b$12$0G2UeNn1UjZkM0d1l1d3A.5wY4rB7nC7zX9kG1vP3oW8eT6rY2q6.', 'pendamping'
WHERE NOT EXISTS (SELECT 1 FROM `pengguna` WHERE `email` = 'pendamping@rapor.tk');
