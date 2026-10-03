# EduRAG Merdeka — Material Design 3 (M3) Design System & UI/UX Specification

> **Versi:** 2.0.0  
> **Standar:** Google Material Design 3 (Material You) & WCAG 2.2 AA Compliance  
> **Identitas Visual:** Sage Green Education (#4F7A56), Warm Pastel Yellow (#F2C94C), Sky Pastel Blue (#6FB8DE)

---

## 1. Filosofi Desain

EduRAG Merdeka dirancang dengan mengadopsi prinsip **Material You (Material 3)** yang disesuaikan khusus untuk lingkungan pembelajaran Indonesia:
- **Tenang & Fokus (*Mindful Education*):** Menggunakan palet hijau alami (*Sage Green*) sebagai warna dominan untuk meredakan ketegangan siswa saat belajar atau guru saat menyusun asesmen.
- **Keterbacaan Tinggi (*Accessible Legibility*):** Tipografi berstandar WCAG 2.2 AA dengan rasio kontras teks minimal 4.5:1 untuk teks normal dan 3:1 untuk teks berukuran besar.
- **Hierarki Berbasis Permukaan Tonal (*Tonal Surface Elevation*):** Menggantikan efek bayangan gelap kaku dengan permukaan warna bertingkat (*Surface Container Lowest* hingga *Highest*).
- **Sitasi Transparan (*Verifiable Truth*):** Desain chip sitasi dan guardrail badge berwarna kontras memastikan setiap fakta dari Buku Teks Kemendikbud langsung terlihat bab dan nomor halamannya.

---

## 2. Palet Warna & Tonal Palette (M3 Color Tokens)

### 2.1 Skema Warna Utama (Light Mode)

| Peran Token M3 | Hex Code | Pratinjau | Nilai Kontras | Penggunaan UI |
| :--- | :--- | :---: | :---: | :--- |
| **`primary`** | `#386A43` / `#4F7A56` | 🟢 | 4.8:1 pada `#FFFFFF` | Header modul, tab aktif, ikon utama, identitas brand. |
| **`on-primary`** | `#FFFFFF` | ⚪ | 4.8:1 pada Primary | Teks di atas tombol primary dan header banner. |
| **`primary-container`** | `#BAECC0` | 🟩 | 11.2:1 dgn Dark | Latar belakang kartu aktif dan badge guardrail valid (>0.70). |
| **`on-primary-container`** | `#00210B` | ⬛ | 11.2:1 | Teks di dalam primary container. |
| **`secondary`** | `#F2C94C` | 🟡 | 8.2:1 dgn `#231B00` | Tombol CTA aksi utama (*Generate Soal*, *Generate RPP*). |
| **`secondary-container`**| `#F7E28C` | 🟨 | 12.0:1 | Status warning, highlight kata kunci penting. |
| **`on-secondary`** | `#221B00` | 🟫 | 8.2:1 | Teks label pada tombol kuning sekunder. |
| **`tertiary`** | `#196584` / `#6FB8DE` | 🔵 | 5.2:1 dgn Surface | Badge Sitasi Buku, link referensi halaman, ekspor file. |
| **`tertiary-container`** | `#C1E8FF` | 🟦 | 12.5:1 dgn Dark | Latar badge sitasi Bab & Halaman buku teks. |
| **`on-tertiary-container`**| `#001E2B` | 🔷 | 12.5:1 | Teks pada badge sitasi halaman. |
| **`error`** | `#BA1A1A` | 🔴 | 5.1:1 | Peringatan materi halusinasi / tidak ditemukan. |
| **`error-container`** | `#FFDAD6` | 🟥 | 11.8:1 | Latar badge guardrail alert (<0.70). |

---

### 2.2 Sistem Elevasi Permukaan Tonal (Tonal Surfaces)

Material 3 tidak mengandalkan drop shadow tebal, melainkan pergeseran kecerahan permukaan (*Tonal Elevation*):

| Level Permukaan | CSS Token | Hex (Light) | Hex (Dark) | Komponen UI |
| :---: | :--- | :--- | :--- | :--- |
| **Level 0** | `--md-sys-color-surface` | `#F7FAF3` | `#101410` | Latar belakang utama aplikasi (*app background*). |
| **Level 1** | `--md-sys-color-surface-container-low` | `#F1F5ED` | `#191D18` | Kolom input pesan, panel samping (*sidebar*). |
| **Level 2** | `--md-sys-color-surface-container` | `#EBEFE7` | `#1D211C` | Kartu materi standar (*default cards*). |
| **Level 3** | `--md-sys-color-surface-container-high` | `#E6EAE2` | `#272B26` | Kartu melayang saat hover (*hover state*). |
| **Level 4** | `--md-sys-color-surface-container-highest`| `#E0E4DC`| `#323631` | Dialog modal, dropdown popover, segmented buttons. |
| **Lowest** | `--md-sys-color-surface-container-lowest` | `#FFFFFF` | `#0C0F0C` | Bubble chat asisten, lembar kertas RPP. |

---

## 3. Sistem Tipografi (M3 Typography Scale)

Kombinasi dua jenis huruf modern:
1. **Brand Font (Heading):** `Plus Jakarta Sans` — Geometris, ramah, dan tegas.
2. **Plain Font (Body & Label):** `Inter` — Netral, jelas di layar HP maupun laptop beresolusi tinggi.

```
Display Large    · Plus Jakarta Sans Bold · 57px · Line: 64px · Tracking: -0.25px
Headline Medium  · Plus Jakarta Sans SemiBold · 28px · Line: 36px · Tracking: 0px
Title Large      · Plus Jakarta Sans SemiBold · 22px · Line: 28px · Tracking: 0px
Body Large       · Inter Regular · 16px · Line: 24px · Tracking: 0.5px
Body Medium      · Inter Regular · 14px · Line: 20px · Tracking: 0.25px
Label Large      · Plus Jakarta Sans Bold · 14px · Line: 20px · Tracking: 0.1px (Buttons)
Label Medium     · Inter SemiBold · 12px · Line: 16px · Tracking: 0.5px (Citation Badges)
```

---

## 4. Sistem Bentuk & Sudut Kelengkungan (M3 Shape Scale)

Material 3 menekankan sudut membulat yang ekspresif:

| Ukuran Bentuk | Radius (`border-radius`) | Penerapan Komponen |
| :--- | :--- | :--- |
| **None** | `0px` | Elemen batas tabel data mentah. |
| **Extra Small** | `4px` | Indikator progres bar, slider track. |
| **Small** | `8px` | Tag sub-topik kecil, checkbox, tooltip. |
| **Medium** | `12px` | Input text box, field chat input. |
| **Large** | `16px` | Kartu modul, kartu soal pilihan ganda, dropdown menu. |
| **Extra Large** | `24px` – `28px` | Dialog pop-up, banner header utama, kartu fitur hero. |
| **Full (Pill)** | `9999px` | Tombol CTA (*Button*), Filter Chips, Citation Badges, Role Switcher. |

---

## 5. Anatomi Komponen Antarmuka Kunci

### 5.1 Role Switcher (Segmented Button M3)
Terletak di bilah samping atau navigasi atas untuk berpindah antara dua dunia pengguna:
```
┌───────────────────────────────────────────────────────────┐
│  (•) 👨‍🎓 Mode Siswa (Tanya)    ( ) 👩‍🏫 Mode Guru (Soal/RPP)   │
└───────────────────────────────────────────────────────────┘
```
- **State Normal:** Background `surface-container-high`, teks muted `#424941`.
- **State Aktif:** Background `primary-container` (`#BAECC0`), teks bold `#00210B`, ikon transisi halus 200ms.

---

### 5.2 Filter Chips Mata Pelajaran (Assist/Filter Chip M3)
Pilihan subjek horizontal dengan ikon tematik:
```
[ 📐 Matematika ]   [ 🔬 IPA Terpadu ]   [ 📖 B. Indonesia ]   [ 🇬🇧 B. Inggris ]
```
- Sudut kelengkungan: `9999px` (Pill shape).
- Tinggi: `36px` dengan padding horizontal `16px`.
- Border aktif: `1.5px solid var(--primary)`.

---

### 5.3 Bubble Chat & Citation Badge (Komponen Khusus EduRAG)
Representasi pesan dari asisten cerdas:
```
┌──────────────────────────────────────────────────────────────────────┐
│  Eksponen adalah perkalian berulang bilangan pokok n kali...         │
│  Logaritma merupakan inversi perpangkatan: ᵃlog b = c <=> aᶜ = b.    │
│                                                                      │
│  [ 📖 Sitasi: Matematika Kelas 10 • Bab 1 • Hal 14 ]                 │
│  [ 🛡️ Cosine Similarity: 0.98 (> 0.70 Lolos Guardrail) ]             │
└──────────────────────────────────────────────────────────────────────┘
```
- **Latar:** `surface-container-lowest` (`#FFFFFF`).
- **Citation Badge:**
  - Background: `#C1E8FF` (Tertiary Container).
  - Teks: `#001E2B` (On-Tertiary Container), font-weight: `600`, ukuran: `12px`.
  - Icon: `📖` (Buku resmi Kemendikbud).
- **Guardrail Badge:**
  - Lolos: `#BAECC0` (Hijau Tonal, similarity > 0.70).
  - Peringatan: `#FFDAD6` (Merah Tonal, alert anti-halusinasi terpicu).

---

### 5.4 Tombol Aksi Utama (M3 Filled & Elevated Button)
```
┌──────────────────────────────────────────────┐
│           ⚡ GENERATE PAKET SOAL             │
└──────────────────────────────────────────────┘
```
- Background: `#F2C94C` (Secondary Warm Pastel Yellow).
- Warna Teks: `#231B00` (Ultra Dark Contrast 8.2:1).
- Bentuk: `9999px` (Pill).
- Efek Hover: `transform: scale(1.02); filter: brightness(1.05);` dengan bayangan `0 4px 12px rgba(242, 201, 76, 0.3)`.

---

## 6. Aksesibilitas & Responsive Breakpoints

1. **Touch Target Size:** Seluruh tombol dan chip interaktif memiliki area sentuh minimal `44px x 44px` sesuai standar WCAG 2.2 AA.
2. **Keyboard Navigation:** Setiap elemen interaktif memiliki `focus-visible` ring berwarna primer (`outline: 2px solid #386A43; outline-offset: 2px`).
3. **Breakpoints Responsif:**
   - **Mobile (Phone):** `< 600px` (Layout 1 kolom, sidebar collapsible).
   - **Tablet:** `600px - 1024px` (Grid 2 kolom untuk bank soal).
   - **Desktop:** `> 1024px` (Max-width 1100px terpusat, dual tab generator).
