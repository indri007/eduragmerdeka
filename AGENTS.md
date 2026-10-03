# EduRAG Merdeka — System Rules & Engineering Guidelines (AGENTS.md)

Dokumen ini mendefinisikan aturan baku (*rules & constraints*) yang wajib dipatuhi oleh seluruh AI Agent, pengembang, dan kontributor dalam proyek **EduRAG Merdeka**.

---

## 1. Aturan Inti AI & Guardrail Anti-Halusinasi

### Rule 1.1: Kewajiban Sitasi Resmi (Mandatory Citation)
- Setiap jawaban yang dihasilkan untuk siswa **WAJIB** menyertakan sitasi resmi yang mencakup:
  1. Nama Buku Resmi (*Buku Siswa* atau *Buku Guru* Kemendikbudristek).
  2. Nomor dan Judul Bab (*e.g., Bab 1: Eksponen dan Logaritma*).
  3. Nomor Halaman Fisik Buku (*e.g., Halaman 14*).
- Dilarang memberikan jawaban konseptual tanpa rujukan buku teks.

### Rule 1.2: Batas Ambang Kemiripan (Cosine Threshold > 0.70)
- Sistem hanya boleh menyusun jawaban apabila skor *Cosine Similarity* antara pertanyaan dengan potongan teks (*chunk*) buku mencapai minimal **$\ge 0.70$**.
- Jika skor $< 0.70$, sistem **WAJIB** memicu penolakan ramah (*Guardrail Alert*):
  > *"Materi tidak ditemukan di buku teks Kurikulum Merdeka Kelas 10. Sistem menolak menjawab demi mencegah halusinasi data."*

### Rule 1.3: Penolakan Pertanyaan Non-Akademik (Off-Topic Filter)
- Pertanyaan di luar cakupan kurikulum (gosip, resep makanan, selebriti, skor olahraga non-pelajaran) harus langsung dihentikan sebelum memanggil LLM untuk efisiensi biaya komputasi dan token.

---

## 2. Aturan Generator Konten Guru (Mode Guru)

### Rule 2.1: Standar Paket Soal HOTS
Setiap eksekusi generator soal ulangan wajib memproduksi tepat format baku berikut:
1. **5 Butir Pilihan Ganda (PG):**
   - 4 Opsi Jawaban (A, B, C, D) dengan satu jawaban benar bertanda `*(Kunci)*`.
   - Disertai paragraf **Pembahasan Konsep** yang merujuk pada halaman buku sumber.
2. **2 Butir Soal Esai HOTS (Higher-Order Thinking Skills):**
   - Berorientasi pemecahan masalah kontekstual dan penalaran kritis.
   - Disertai **Rubrik Penilaian Objektif (Skor Maksimal 10)** per soal.

### Rule 2.2: Standar Draf Modul Ajar (RPP Deep Learning)
Draf RPP wajib mengikuti regulasi Kurikulum Merdeka Fase E (Kelas 10) dengan 3 komponen inti:
1. **Tujuan Pembelajaran (TP):** Selaras dengan Capaian Pembelajaran (CP) dan Profil Pelajar Pancasila.
2. **Langkah Kegiatan Pembelajaran:** Menggunakan model *Problem-Based Learning (PBL)* atau *Inkuiri Terbimbing* (Pendahuluan, 5 Sintaks Inti PBL, Penutup).
3. **Instrumen Asesmen Lengkap:** Asesmen Diagnostik, Asesmen Formatif (Observasi Sikap), dan Asesmen Sumatif (Kuis Soal).

---

## 3. Aturan Desain UI/UX (Material Design 3)

### Rule 3.1: Konsistensi Palet Warna M3
Dilarang menggunakan warna generik/mentah (*plain blue, red*). Gunakan selalu token warna resmi:
- **Primary:** `#4F7A56` / `#386A43` (Sage Green) & Container `#BAECC0`
- **Secondary:** `#F2C94C` (Warm Pastel Yellow) untuk tombol CTA
- **Tertiary:** `#6FB8DE` / `#C1E8FF` (Sky Pastel Blue) khusus badge sitasi buku
- **Background / Surface:** `#F4F8F1` / `#FFFFFF`

### Rule 3.2: Tipografi Resmi
- **Headings & Judul:** `Plus Jakarta Sans` (Bobot 600–800)
- **Body Text & Soal:** `Inter` (Bobot 400–500)
- Rasio kontras teks wajib memenuhi standar aksesibilitas **WCAG 2.2 AA ($\ge 4.5:1$)**.

### Rule 3.3: Komponen Bentuk (Shape)
- Seluruh tombol utama, kapsul sitasi, dan tab pengalih peran harus bertipe **Full Pill** (`border-radius: 9999px`).
- Kartu materi dan kotak dialog menggunakan radius sedang hingga besar (`16px` – `24px`).

---

## 4. Aturan Keamanan & Manajemen Rahasia (Security Rules)

### Rule 4.1: Larangan Keras Komit API Key / Rahasia
- **JANGAN PERNAH** menuliskan atau melakukan git commit terhadap token, kata sandi, atau API Key asli (`ghp_*`, `COHERE_API_KEY`, `QDRANT_API_KEY`, `.env`).
- Seluruh berkas rahasia wajib terdaftar di `.gitignore`.
- Konfigurasi rahasia pada Streamlit Cloud wajib menggunakan panel bawaan:  
  **App Settings $\rightarrow$ Secrets (`secrets.toml`)**.

---

## 5. Standar Kode & Git Workflow

### Rule 5.1: Konvensi Pesan Commit
Gunakan format *Conventional Commits*:
- `feat:` Penambahan fitur baru (misal: generator kuis baru, filter chip)
- `fix:` Perbaikan bug atau kesalahan retrieval
- `docs:` Pembaruan dokumentasi, PRD, atau skema
- `style:` Penyesuaian CSS / Material 3 styling
- `security:` Penguatan `.gitignore` atau audit dependensi

### Rule 5.2: Uji Pra-Rilis (Zero Error Execution)
Sebelum melakukan `git push` ke branch `main`, pastikan:
1. `python3 -m py_compile streamlit_app.py` menghasilkan kode keluar 0.
2. Tidak ada jalur dependensi yang rusak pada `requirements.txt`.
