-- =============================================================================
-- EduRAG Merdeka — Production Database Schema
-- Dialect: MySQL 8.0+ / MariaDB / Aiven MySQL / Cloud SQL Compatible
-- Encoding: UTF-8 Unicode (utf8mb4 / utf8mb4_unicode_ci)
-- =============================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- -----------------------------------------------------------------------------
-- 1. Table: mapel (Mata Pelajaran Kurikulum Merdeka)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `mapel`;
CREATE TABLE `mapel` (
    `mapel_id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama_mapel` VARCHAR(100) NOT NULL COMMENT 'Contoh: Matematika, IPA Terpadu',
    `kode_mapel` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Contoh: MAT-X, IPA-X',
    `fase` VARCHAR(20) NOT NULL DEFAULT 'Fase E' COMMENT 'Tingkat Fase Kurikulum Merdeka',
    `deskripsi` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 2. Table: buku (Katalog Buku Siswa & Buku Guru Resmi Kemendikbud)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `buku`;
CREATE TABLE `buku` (
    `buku_id` INT AUTO_INCREMENT PRIMARY KEY,
    `mapel_id` INT NOT NULL,
    `jenis_buku` ENUM('BS', 'BG') NOT NULL COMMENT 'BS: Buku Siswa, BG: Buku Guru',
    `judul_resmi` VARCHAR(255) NOT NULL,
    `penerbit` VARCHAR(150) NOT NULL DEFAULT 'Pusat Perbukuan Kemendikbudristek',
    `tahun_terbit` INT NOT NULL DEFAULT 2022,
    `total_halaman` INT NOT NULL DEFAULT 0,
    `file_pdf_url` VARCHAR(500) NULL,
    `checksum_sha256` VARCHAR(64) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`mapel_id`) REFERENCES `mapel` (`mapel_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 3. Table: bab (Struktur Bab & Capaian Pembelajaran)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `bab`;
CREATE TABLE `bab` (
    `bab_id` INT AUTO_INCREMENT PRIMARY KEY,
    `buku_id` INT NOT NULL,
    `nomor_bab` INT NOT NULL,
    `judul_bab` VARCHAR(255) NOT NULL,
    `elemen_cp` VARCHAR(255) NULL COMMENT 'Elemen Capaian Pembelajaran',
    `halaman_awal` INT NOT NULL,
    `halaman_akhir` INT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`buku_id`) REFERENCES `buku` (`buku_id`) ON DELETE CASCADE,
    INDEX `idx_buku_nomor` (`buku_id`, `nomor_bab`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 4. Table: chunk (Potongan Teks Dokumen untuk RAG)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `chunk`;
CREATE TABLE `chunk` (
    `chunk_id` VARCHAR(64) PRIMARY KEY COMMENT 'UUID / Hash SHA256 teks unik',
    `bab_id` INT NOT NULL,
    `halaman` INT NOT NULL COMMENT 'Nomor halaman fisik pada buku cetak/PDF',
    `isi_teks` MEDIUMTEXT NOT NULL COMMENT 'Cuplikan teks 500-800 token ber-overlap',
    `sub_topik` VARCHAR(255) NULL COMMENT 'Sub-judul bab / topik inti',
    `token_count` INT NOT NULL DEFAULT 0,
    `qdrant_point_id` VARCHAR(64) NULL COMMENT 'Point ID pada koleksi vektor Qdrant',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`bab_id`) REFERENCES `bab` (`bab_id`) ON DELETE CASCADE,
    INDEX `idx_bab_halaman` (`bab_id`, `halaman`),
    FULLTEXT INDEX `idx_ft_isi_teks` (`isi_teks`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 5. Table: user (Pengguna Platform)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `user_id` VARCHAR(64) PRIMARY KEY COMMENT 'UUID akun pengguna',
    `nama` VARCHAR(150) NOT NULL,
    `email` VARCHAR(150) UNIQUE NOT NULL,
    `role` ENUM('siswa', 'guru', 'admin') NOT NULL DEFAULT 'siswa',
    `asal_sekolah` VARCHAR(200) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 6. Table: chat_history (Log Sesi Tanya Jawab & Skor Guardrail)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `chat_history`;
CREATE TABLE `chat_history` (
    `chat_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` VARCHAR(64) NOT NULL,
    `mapel_id` INT NOT NULL,
    `query_siswa` TEXT NOT NULL,
    `response_rag` MEDIUMTEXT NOT NULL,
    `cosine_similarity` DECIMAL(5, 4) NOT NULL COMMENT 'Cosine threshold batas > 0.70',
    `guardrail_passed` BOOLEAN NOT NULL DEFAULT TRUE,
    `latency_ms` INT NOT NULL DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`mapel_id`) REFERENCES `mapel` (`mapel_id`) ON DELETE CASCADE,
    INDEX `idx_user_time` (`user_id`, `created_at`),
    INDEX `idx_guardrail` (`guardrail_passed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 7. Table: citation (Sitasi Resmi Buku Asli pada Respon Chat)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `citation`;
CREATE TABLE `citation` (
    `citation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `chat_id` INT NOT NULL,
    `chunk_id` VARCHAR(64) NOT NULL,
    `nomor_halaman` INT NOT NULL,
    `label_bab` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`chat_id`) REFERENCES `chat_history` (`chat_id`) ON DELETE CASCADE,
    FOREIGN KEY (`chunk_id`) REFERENCES `chunk` (`chunk_id`) ON DELETE CASCADE,
    INDEX `idx_chat_citation` (`chat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- 8. Table: generated_content (Hasil Generator Soal HOTS & Modul Ajar RPP)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS `generated_content`;
CREATE TABLE `generated_content` (
    `content_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` VARCHAR(64) NOT NULL,
    `bab_id` INT NOT NULL,
    `tipe_konten` ENUM('soal_hots', 'modul_ajar_rpp') NOT NULL,
    `payload_json` LONGTEXT NOT NULL COMMENT 'JSON terstruktur 5 PG + 2 Esai atau RPP',
    `export_filename` VARCHAR(255) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
    FOREIGN KEY (`bab_id`) REFERENCES `bab` (`bab_id`) ON DELETE CASCADE,
    INDEX `idx_guru_tipe` (`user_id`, `tipe_konten`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------------------------------
-- 9. Initial Seed Data (Data Awal Kurikulum Merdeka Kelas 10)
-- -----------------------------------------------------------------------------
INSERT INTO `mapel` (`mapel_id`, `nama_mapel`, `kode_mapel`, `fase`, `deskripsi`) VALUES
(1, 'Matematika', 'MAT-X', 'Fase E', 'Matematika SMA Kelas 10 Kurikulum Merdeka'),
(2, 'IPA Terpadu', 'IPA-X', 'Fase E', 'Fisika, Kimia, dan Biologi Terpadu Kelas 10'),
(3, 'Bahasa Indonesia', 'BIN-X', 'Fase E', 'Bahasa dan Sastra Indonesia Kelas 10'),
(4, 'Bahasa Inggris', 'ENG-X', 'Fase E', 'English for Change Kelas 10 SMA');

INSERT INTO `buku` (`buku_id`, `mapel_id`, `jenis_buku`, `judul_resmi`, `tahun_terbit`) VALUES
(1, 1, 'BS', 'Matematika untuk SMA/SMK Kelas X', 2022),
(2, 2, 'BS', 'Ilmu Pengetahuan Alam untuk SMA Kelas X', 2022),
(3, 3, 'BS', 'Cerdas Cergas Berbahasa dan Bersastra Indonesia Kelas X', 2022),
(4, 4, 'BS', 'Work in Progress: English for SMA/SMK Grade X', 2022);

INSERT INTO `bab` (`bab_id`, `buku_id`, `nomor_bab`, `judul_bab`, `elemen_cp`, `halaman_awal`, `halaman_akhir`) VALUES
(1, 1, 1, 'Eksponen dan Logaritma', 'Bilangan & Aljabar', 1, 35),
(2, 1, 2, 'Vektor dan Operasinya', 'Geometri', 36, 68),
(3, 1, 6, 'Statistika dan Diagram Data', 'Analisis Data & Peluang', 145, 185),
(4, 2, 1, 'Pengukuran dalam Kerja Ilmiah', 'Keterampilan Proses Sains', 1, 30),
(5, 2, 8, 'Pemanasan Global dan Perubahan Iklim', 'Pemahaman Sains', 175, 210),
(6, 2, 6, 'Energi Terbarukan', 'Energi & Perubahan', 125, 155),
(7, 3, 1, 'Mengungkap Fakta Alam (Teks LHO)', 'Menyimak & Membaca', 1, 32),
(8, 3, 4, 'Belajar Menegosiasikan Kepentingan', 'Berbicara & Mempresentasikan', 85, 120),
(9, 4, 1, 'Unit 1: Great Athletes (Descriptive Text)', 'Reading & Viewing', 1, 25);
