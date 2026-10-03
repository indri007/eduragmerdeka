# 🎓 EduRAG Merdeka

> **Platform AI Interaktif RAG & Generator Pembelajaran Berbasis Kurikulum Merdeka Kelas 10 (Fase E)**  
> *Solusi Cerdas untuk Siswa & Guru: Bebas Halusinasi, Tersitasi Presisi, dan Menghemat Waktu Administrasi.*

---

## 🌟 Fitur Utama

### 👨‍🎓 1. Mode Siswa (Tanya-Jawab Terverifikasi)
* **Tanya Materi Kontekstual**: Siswa dapat menanyakan konsep mata pelajaran (**Matematika**, **IPA Terpadu**, **Bahasa Indonesia**, **Bahasa Inggris**) dengan bahasa sehari-hari.
* **Sitasi Presisi (Bab & Halaman)**: Setiap jawaban menyertakan badge sitasi langsung ke halaman buku teks resmi.
* **Anti-Halusinasi Guardrail**: Cosine similarity threshold > 0.70. Jika pertanyaan di luar konteks buku, sistem langsung menjawab *"Materi tidak ditemukan di buku, coba kata kunci lain"* tanpa spekulasi generatif liar.

### 👩‍🏫 2. Mode Guru (Generator Soal & Draf Modul Ajar)
* **Generator Paket Soal**: Menghasilkan 5 Soal Pilihan Ganda (dengan opsi A–D, kunci jawaban, dan pembahasan mendalam) + 2 Soal Esai HOTS per bab spesifik.
* **Generator Modul Ajar (RPP)**: Menyusun draf Modul Ajar terstruktur baku (Tujuan Pembelajaran, Langkah-Langkah Kegiatan Pembelajaran, Asesmen Diagnostik/Formatif/Sumatif) yang selaras dengan Capaian Pembelajaran (CP) dan Alur Tujuan Pembelajaran (ATP).
* **Smart Cache & Reuse**: Mendeteksi bab yang sudah pernah dibuat untuk menghemat kuota pemanggilan API.
* **Ekspor Cepat**: Salin teks atau unduh draf ke format dokumen.

---

## 🏗️ Arsitektur & Teknologi

* **Frontend & Interaksi**: Streamlit / Python dengan Custom CSS (*Design System Kurikulum Merdeka*: Pastel Green `#7FAE83`, Pastel Yellow `#F2C94C`, Pastel Blue `#6FB8DE`).
* **Vector Store**: Qdrant Vector Search Engine (`kurikulum_merdeka_kelas10`).
* **Relational Database**: MySQL (Aiven) / SQLite kompatibel (`mapel`, `buku`, `bab`, `chunk`, `user`, `chat_history`, `citation`, `generated_content`).
* **Embedding & Reranker**: `BAAI/bge-m3` & `BAAI/bge-reranker-v2-m3` / Gemini Embeddings.
* **Inference LLM**: Google Gemini 2.5 Flash / 1.5 Flash & Sahabat-AI.
* **PDF Parser**: Docling & PyMuPDF untuk ekstraksi tata letak, tabel, dan hierarki bab.
* **Evaluasi**: RAGAS + Benchmark `IDK-MRC` & `IndoMMLU`.

---

## 📂 Struktur Repositori

```text
eduragmerdeka/
├── docs/
│   └── PRD_EduRAG_Merdeka.md     # Spesifikasi PRD, ERD, Schema, & Rules Lengkap
├── src/
│   ├── db/                        # Manajemen database relasional & schema
│   ├── rag/                       # Qdrant client, retrieval, guardrail & reranker
│   ├── generator/                 # Modul generator soal & draf RPP
│   ├── ingestion/                 # Pipeline ekstraksi PDF & chunking
│   └── ui/                        # Komponen Streamlit & styling design system
├── app.py                         # Aplikasi utama Streamlit
├── requirements.txt               # Dependensi proyek
├── .gitignore
└── README.md
```

---

## 🌐 Landing Page (GitHub Pages)

Landing page proyek ini dibangun dengan standar **Material Design 3 (Material You)**, aksesibilitas **WCAG 2.2 AA**, dan performa tinggi (zero-framework, HTML/CSS/JS statis murni).

* **Live URL**: [https://indri007.github.io/eduragmerdeka/](https://indri007.github.io/eduragmerdeka/)
* **Files**: `index.html`, `styles.css`, `main.js`, `assets/`

### Kustomisasi Warna & Tema
Seluruh token warna Material 3 didefinisikan sebagai CSS Custom Properties di bagian atas [`styles.css`](styles.css):
* **Seed Color**: `#4F7A56` (Deep Green)
* **Secondary**: `#F2C94C` (Pastel Yellow)
* **Tertiary**: `#6FB8DE` (Pastel Blue)

Untuk mengubah warna tema, cukup ubah nilai variabel CSS `:root` (untuk Light Theme) dan `[data-theme="dark"]` (untuk Dark Theme) di `styles.css`.

### Deployment Otomatis ke GitHub Pages
Proyek ini menyertakan GitHub Actions workflow di [`.github/workflows/pages.yml`](.github/workflows/pages.yml). Setiap kali perubahan di-push ke branch `main`, landing page akan otomatis ter-build dan terpublikasi ke GitHub Pages.

---

## 📖 Dokumentasi Lengkap
Dokumentasi lengkap mengenai arsitektur, ERD, skema database, palet warna, dan aturan sistem dapat dilihat di:  
👉 [docs/PRD_EduRAG_Merdeka.md](docs/PRD_EduRAG_Merdeka.md)

