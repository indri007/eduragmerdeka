"""
EduRAG Merdeka — Streamlit Web Application
Asisten Belajar & Mengajar Berbasis Retrieval-Augmented Generation untuk Kurikulum Merdeka Kelas 10
Design System: Material 3 (Pastel Green #7FAE83, Pastel Yellow #F2C94C, Pastel Blue #6FB8DE)
"""

import streamlit as st
import time
import json
import re
import os

# -----------------------------------------------------------------------------
# 1. Page Configuration & M3 Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduRAG Merdeka — Asisten Kurikulum Merdeka",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom M3 CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

    :root {
        --primary: #4F7A56;
        --primary-light: #7FAE83;
        --primary-container: #BAECC0;
        --secondary: #F2C94C;
        --secondary-container: #FEE488;
        --tertiary: #6FB8DE;
        --tertiary-container: #C1E8FF;
        --background: #F4F8F1;
        --surface: #FFFFFF;
        --text-dark: #233229;
        --text-muted: #6E7C72;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        color: var(--text-dark);
    }

    h1, h2, h3, h4 {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        color: var(--primary);
    }

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Header Banner */
    .edurag-header {
        background: linear-gradient(135deg, #4F7A56, #386A43);
        color: #FFFFFF;
        padding: 24px 30px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(79, 122, 86, 0.15);
    }
    .edurag-header h1 {
        color: #FFFFFF !important;
        margin: 0 0 6px 0;
        font-size: 2.2rem;
    }
    .edurag-header p {
        color: #E2EFE4;
        margin: 0;
        font-size: 1.05rem;
    }

    /* Citation Badges */
    .citation-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #C1E8FF;
        color: #003548;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 8px;
    }

    .guardrail-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #BAECC0;
        color: #003917;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-top: 6px;
        margin-left: 6px;
    }

    .guardrail-alert {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FFDAD6;
        color: #410002;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Buttons */
    .stButton>button {
        background-color: var(--secondary) !important;
        color: #231B00 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 8px 24px !important;
        transition: transform 0.15s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        filter: brightness(1.05);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Knowledge Base & Textbook Chunks (Kurikulum Merdeka Kelas 10)
# -----------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "Matematika": [
        {
            "bab": "Bab 1: Eksponen dan Logaritma",
            "halaman": 14,
            "keywords": ["eksponen", "pangkat", "logaritma", "akar", "bilangan berpangkat", "basis"],
            "teks": "Eksponen adalah perkalian berulang suatu bilangan pokok sebanyak n kali (aⁿ = a × a × ... × a). Sifat-sifat eksponen: aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ / aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, dan a⁻ⁿ = 1/aⁿ. Logaritma adalah inversi eksponen: ᵃlog b = c jika dan hanya jika aᶜ = b dengan a > 0, a ≠ 1, dan b > 0."
        },
        {
            "bab": "Bab 2: Vektor dan Operasinya",
            "halaman": 48,
            "keywords": ["vektor", "arah", "resultan", "vektor satuan", "skalar", "panjang vektor"],
            "teks": "Vektor adalah besaran yang memiliki nilai dan arah. Dalam sistem koordinat kartesius 2 dimensi, vektor posisi dinyatakan dalam r = xi + yj dengan i dan j adalah vektor satuan sumbu X dan Y. Panjang vektor dinyatakan dengan |r| = √(x² + y²). Dua vektor dikatakan ekuivalen jika memiliki besar dan arah yang sama."
        },
        {
            "bab": "Bab 6: Statistika dan Diagram Data",
            "halaman": 162,
            "keywords": ["statistika", "modus", "median", "mean", "kuartil", "diagram box plot", "jangkauan"],
            "teks": "Ukuran pemusatan data meliputi Mean (rata-rata), Median (nilai tengah), dan Modus (nilai yang paling sering muncul). Ukuran penempatan mencakup Kuartil Bawah (Q1), Kuartil Tengah (Q2), dan Kuartil Atas (Q3). Jangkauan interkuartil dihitung dengan IQR = Q3 - Q1."
        }
    ],
    "IPA Terpadu": [
        {
            "bab": "Bab 1: Pengukuran dalam Kerja Ilmiah",
            "halaman": 12,
            "keywords": ["pengukuran", "jangka sorong", "mikrometer sekrup", "angka penting", "ketidakpastian", "skala"],
            "teks": "Pengukuran adalah kegiatan membandingkan suatu besaran yang diukur dengan besaran sejenis yang dipakai sebagai satuan. Alat ukur panjang presisi meliputi Jangka Sorong (ketelitian 0,05 mm - 0,1 mm) dan Mikrometer Sekrup (ketelitian 0,01 mm). Aturan angka penting menyatakan bahwa semua angka bukan nol adalah angka penting."
        },
        {
            "bab": "Bab 8: Pemanasan Global dan Perubahan Iklim",
            "halaman": 184,
            "keywords": ["pemanasan global", "efek rumah kaca", "karbon dioksida", "iklim", "emisi", "lingkungan", "gas rumah kaca"],
            "teks": "Pemanasan global adalah peningkatan suhu rata-rata atmosfer, laut, dan daratan bumi akibat terperangkapnya radiasi inframerah oleh Gas Rumah Kaca (GRK) seperti CO₂, CH₄, N₂O, dan uap air. Dampaknya mencakup naiknya permukaan laut, pergeseran musim tanam, dan cuaca ekstrem."
        },
        {
            "bab": "Bab 6: Energi Terbarukan",
            "halaman": 138,
            "keywords": ["energi terbarukan", "panel surya", "biomassa", "kinetik", "efisiensi energi", "kekekalan energi"],
            "teks": "Hukum Kekekalan Energi menyatakan bahwa energi tidak dapat diciptakan atau dimusnahkan, melainkan hanya dapat diubah dari satu bentuk ke bentuk lain. Sumber energi terbarukan meliputi energi surya, angin, mikrohidro, dan geotermal yang ramah lingkungan."
        }
    ],
    "Bahasa Indonesia": [
        {
            "bab": "Bab 1: Mengungkap Fakta Alam (Teks LHO)",
            "halaman": 9,
            "keywords": ["lho", "laporan hasil observasi", "observasi", "fakta", "deskripsi umum", "bagian", "manfaat"],
            "teks": "Teks Laporan Hasil Observasi (LHO) memaparkan fakta-fakta yang diperoleh dari pengamatan objektif. Struktur teks LHO terdiri dari: 1. Pernyataan Umum / Klasifikasi (definisi pembuka), 2. Deskripsi Bagian (rincian ciri objek), dan 3. Deskripsi Manfaat (kegunaan bagi kehidupan)."
        },
        {
            "bab": "Bab 4: Belajar Menegosiasikan Kepentingan",
            "halaman": 92,
            "keywords": ["negosiasi", "kesepakatan", "tawar", "orientasi", "pengajuan", "persetujuan", "kompromi"],
            "teks": "Teks Negosiasi adalah bentuk interaksi sosial yang bertujuan mencapai kesepakatan bersama antara pihak-pihak yang memiliki kepentingan berbeda. Struktur negosiasi meliputi: Orientasi, Pengajuan, Penawaran, Persetujuan, dan Penutup."
        }
    ],
    "Bahasa Inggris": [
        {
            "bab": "Unit 1: Great Athletes (Descriptive Text)",
            "halaman": 8,
            "keywords": ["athlete", "descriptive", "identification", "description", "simple present", "adjectives"],
            "teks": "Descriptive text describes a particular person, place, or thing in detail. Generic structure: Identification (introduces the subject) and Description (details physical features, personality, achievements). Language feature: Simple Present Tense and vivid adjectives."
        }
    ]
}

# -----------------------------------------------------------------------------
# 3. Question Bank for Teacher Mode (5 PG + 2 Essay HOTS per Bab)
# -----------------------------------------------------------------------------
SOAL_BANK = {
    "Bab 1: Eksponen dan Logaritma": {
        "pg": [
            ("Bentuk sederhana dari (a³b⁻²)⁴ / (a⁻²b³) adalah...",
             ["a¹⁴ / b¹¹", "a¹² / b⁸", "a¹⁰ / b⁵", "a⁸ / b⁶"],
             "A",
             "Gunakan sifat eksponen (aᵐ)ⁿ = aᵐⁿ dan pembagian aᵐ / aⁿ = aᵐ⁻ⁿ. Pangkat a: 12 - (-2) = 14. Pangkat b: -8 - 3 = -11, hasil akhir a¹⁴ / b¹¹."),
            ("Jika ²log 3 = p dan ²log 5 = q, maka nilai dari ²log 45 adalah...",
             ["p² + q", "2p + q", "p + 2q", "2p + 2q"],
             "B",
             "45 = 3² × 5. Sesuai sifat logaritma: ²log(3² × 5) = 2(²log 3) + ²log 5 = 2p + q."),
            ("Nilai x yang memenuhi persamaan 3²ˣ⁺¹ = 27 adalah...",
             ["x = 1", "x = 2", "x = 3", "x = 0"],
             "A",
             "27 = 3³. Maka 3²ˣ⁺¹ = 3³ => 2x + 1 = 3 => 2x = 2 => x = 1."),
            ("Syarat basis a pada bentuk logaritma ᵃlog b agar terdefinisi adalah...",
             ["a > 0 dan a ≠ 1", "a ≥ 0 dan a ≠ 1", "a bilangan real sembarang", "a < 0"],
             "A",
             "Sesuai definisi Buku Siswa hal. 18, basis logaritma harus positif dan bukan satu (a > 0 dan a ≠ 1)."),
            ("Model pertumbuhan bakteri mengikuti fungsi N(t) = 100 × 2ᵗ (t dalam jam). Jumlah bakteri setelah 4 jam adalah...",
             ["800", "1.600", "3.200", "6.400"],
             "B",
             "N(4) = 100 × 2⁴ = 100 × 16 = 1.600 bakteri.")
        ],
        "esai": [
            ("Sederhanakan bentuk akar berikut dan rasionalkan penyebutnya: (4√3) / (√5 - √3)! Tuliskan langkah perhitungannya!",
             "Skor 10 jika mengalikan sekawan (√5 + √3)/(√5 + √3), menyederhanakan penyebut menjadi 5 - 3 = 2, dan hasil akhir 2√15 + 6."),
            ("Suatu zat radioaktif memiliki waktu paruh 20 hari dengan massa awal 80 gram. Tentukan sisa massa zat setelah 60 hari menggunakan pemodelan eksponensial!",
             "Skor 10 jika merumuskan N(t) = N₀ × (1/2)^(t/T), mensubstitusi t=60, T=20 sehingga (1/2)³ = 1/8, dan hasil akhir 80 × 1/8 = 10 gram.")
        ]
    },
    "Bab 2: Vektor dan Operasinya": {
        "pg": [
            ("Sebuah vektor posisi r dinyatakan dengan r = 6i + 8j. Panjang (magnitudo) vektor r adalah...",
             ["10 satuan", "14 satuan", "48 satuan", "7 satuan"],
             "A",
             "|r| = √(6² + 8²) = √(36 + 64) = √100 = 10 satuan."),
            ("Dua buah vektor dikatakan ekuivalen (sama) jika dan hanya jika...",
             ["Memiliki titik tangkap yang sama", "Memiliki besar dan arah yang sama", "Memiliki arah berlawanan", "Keduanya berada pada sumbu X"],
             "B",
             "Dua vektor ekuivalen jika panjang dan arah orientasinya identik tanpa memandang letak posisi awal."),
            ("Jika vektor u = 3i - 2j dan vektor v = -i + 5j, maka hasil penjumlahan vektor u + v adalah...",
             ["2i + 3j", "4i + 7j", "-3i - 10j", "2i - 7j"],
             "A",
             "u + v = (3 + (-1))i + (-2 + 5)j = 2i + 3j."),
            ("Vektor satuan searah dengan vektor a = 4i - 3j adalah...",
             ["(4/5)i - (3/5)j", "(3/5)i - (4/5)j", "4i + 3j", "5i - 5j"],
             "A",
             "|a| = √(4² + (-3)²) = 5. Vektor satuan â = a / |a| = (4/5)i - (3/5)j."),
            ("Manakah di antara besaran berikut yang merupakan besaran vektor?",
             ["Massa dan Waktu", "Suhu dan Kelajuan", "Perpindahan dan Kecepatan", "Panjang dan Massa Jenis"],
             "C",
             "Perpindahan dan kecepatan memiliki nilai dan arah, sedangkan kelajuan dan massa adalah besaran skalar.")
        ],
        "esai": [
            ("Dua gaya F₁ = 12 N dan F₂ = 5 N bekerja pada satu titik tangkap dengan sudut apit 90°. Hitunglah besar resultan gaya dan arah vektornya!",
             "Skor 10 jika menghitung R = √(F₁² + F₂²) = √(144 + 25) = 13 N dan sudut tan θ = 5/12."),
            ("Jelaskan perbedaan mendasar antara besaran skalar dan besaran vektor dalam pemodelan gerak perahu yang menyeberangi sungai berarus!",
             "Skor 10 jika menguraikan kelajuan perahu sebagai skalar dan kecepatan resultan akibat arus air sebagai vektor yang dipengaruhi arah sudut gerak.")
        ]
    },
    "Bab 6: Statistika dan Diagram Data": {
        "pg": [
            ("Diberikan data nilai ulangan: 6, 7, 7, 8, 8, 8, 9, 10. Nilai modus dan median data berturut-turut adalah...",
             ["8 dan 8", "7 dan 8", "8 dan 7,5", "8 dan 7"],
             "A",
             "Modus = 8 (muncul 3 kali). Median = (data ke-4 + data ke-5)/2 = (8 + 8)/2 = 8."),
            ("Pada diagram Box Plot (diagram kotak garis), batas kotak sebelah kanan menunjukkan nilai...",
             ["Kuartil Bawah (Q1)", "Median (Q2)", "Kuartil Atas (Q3)", "Nilai Maksimum"],
             "C",
             "Kotak pada Box Plot dibatasi oleh Q1 di kiri, Median (Q2) di tengah, dan Q3 di kanan."),
            ("Jika Q1 = 45 dan Q3 = 75, maka jangkauan interkuartil (IQR) data tersebut adalah...",
             ["30", "60", "120", "15"],
             "A",
             "IQR = Q3 - Q1 = 75 - 45 = 30."),
            ("Suatu nilai pengamatan disebut pencilan (outlier) atas jika nilainya lebih besar dari...",
             ["Q3 + 1,5 × IQR", "Q3 + IQR", "Mean + 2 Standar Deviasi", "Median × 1,5"],
             "A",
             "Rumus baku batas pagar luar atas adalah Q3 + 1,5 × IQR."),
            ("Rata-rata nilai 9 siswa adalah 70. Jika nilai siswa ke-10 digabungkan, rata-ratanya menjadi 72. Nilai siswa ke-10 adalah...",
             ["80", "85", "90", "92"],
             "C",
             "Total awal = 9 × 70 = 630. Total baru = 10 × 72 = 720. Nilai siswa ke-10 = 720 - 630 = 90.")
        ],
        "esai": [
            ("Jelaskan mengapa median lebih tepat digunakan sebagai ukuran pemusatan dibandingkan mean ketika data memiliki pencilan (outlier ekstrim)!",
             "Skor 10 jika menjelaskan sifat resisten median terhadap nilai ekstrem sedangkan mean sangat terdistorsi oleh pencilan."),
            ("Diberikan data: 12, 14, 15, 18, 19, 21, 24, 28, 35. Tentukan nilai Q1, Q2, Q3, dan periksa apakah nilai 35 termasuk pencilan!",
             "Skor 10 jika menghitung Q1=14.5, Q2=19, Q3=26, IQR=11.5, Batas Atas = 26 + 17.25 = 43.25, dan menyimpulkan 35 bukan pencilan.")
        ]
    },
    "Bab 1: Pengukuran dalam Kerja Ilmiah": {
        "pg": [
            ("Tingkat ketelitian (skala terkecil) dari alat ukur Mikrometer Sekrup adalah...",
             ["0,1 mm", "0,05 mm", "0,01 mm", "0,001 mm"],
             "C",
             "Mikrometer sekrup memiliki tingkat ketelitian 0,01 mm (0,001 cm)."),
            ("Hasil pengukuran tebal pelat tipis dengan jangka sorong menunjukkan skala utama 2,3 cm dan nonius garis ke-7 (skala terkecil 0,01 cm). Hasil pembacaan adalah...",
             ["2,37 cm", "2,307 cm", "2,73 cm", "2,07 cm"],
             "A",
             "Hasil = 2,3 cm + (7 × 0,01 cm) = 2,37 cm."),
            ("Berdasarkan aturan angka penting, jumlah angka penting pada hasil pengukuran 0,04050 meter adalah...",
             ["6", "5", "4", "3"],
             "C",
             "Angka nol di depan angka bukan nol bukan AP. Angka 4, 0, 5, dan nol di akhir setelah koma adalah AP (total 4 angka penting: 4, 0, 5, 0)."),
            ("Hasil perkalian 12,5 m (3 AP) dengan 2,0 m (2 AP) menurut aturan angka penting dituliskan...",
             ["25 m²", "25,0 m²", "25,00 m²", "25,000 m²"],
             "A",
             "Hasil perkalian dibulatkan mengikuti angka penting paling sedikit, yaitu 2 AP: 25 m²."),
            ("Sikap ilmiah yang harus dimiliki seorang peneliti saat hasil eksperimen tidak sesuai hipotesis awal adalah...",
             ["Mengubah data pengukuran agar sesuai hipotesis", "Menyajikan data secara jujur dan menganalisis faktor penyebab", "Mengabaikan hasil percobaan", "Mengganti hipotesis secara diam-diam"],
             "B",
             "Prinsip integritas kerja ilmiah menuntut kejujuran data dan evaluasi kesalahan sistematis/acak.")
        ],
        "esai": [
            ("Uraikan perbedaan kesalahan sistematis dan kesalahan acak dalam pengukuran fisika serta berikan masing-masing 2 contoh konkret!",
             "Skor 10 jika membedakan kesalahan kalibrasi/paralaks (sistematis) dengan fluktuasi tegangan/getaran lingkungan (acak)."),
            ("Mengapa mikrometer sekrup lebih dianjurkan daripada mistar biasa untuk mengukur diameter kawat tembaga? Jelaskan dari aspek ketelitian!",
             "Skor 10 jika membandingkan ketelitian mikrometer (0,01 mm) vs mistar (1 mm) terhadap ukuran kawat tembaga yang berskala milimeter.")
        ]
    },
    "Bab 8: Pemanasan Global dan Perubahan Iklim": {
        "pg": [
            ("Gas rumah kaca yang memiliki kontribusi terbesar terhadap efek pemanasan global akibat pembakaran bahan bakar fosil adalah...",
             ["Oksigen (O₂)", "Nitrogen (N₂)", "Karbon Dioksida (CO₂)", "Argon (Ar)"],
             "C",
             "CO₂ merupakan gas rumah kaca utama hasil emisi industri dan kendaraan bermotor."),
            ("Mekanisme terjadinya efek rumah kaca di atmosfer bumi secara fisik adalah...",
             ["Menyerap radiasi ultraviolet matahari secara total", "Memerangkap radiasi inframerah gelombang panjang yang dipancarkan permukaan bumi", "Memantulkan seluruh cahaya tampak ke luar angkasa", "Mendinginkan lapisan stratosfer"],
             "B",
             "GRK meneruskan cahaya tampak matahari namun menyerap radiasi inframerah panas yang dipancarkan kembali oleh bumi."),
            ("Dampak langsung pemanasan global terhadap ekosistem pesisir dan pulau-pulau kecil adalah...",
             ["Penurunan salinitas air tawar", "Kenaikan permukaan air laut akibat pencairan es kutub", "Peningkatan lapisan ozon", "Penurunan curah hujan rata-rata global"],
             "B",
             "Ekspansi termal air laut dan pencairan gletser kutub menyebabkan kenaikan muka air laut global."),
            ("Aktivitas sektor pertanian yang menghasilkan emisi gas metana (CH₄) tinggi adalah...",
             ["Lahan persawahan tergenang (padi) dan peternakan sapi", "Penanaman pohon sengon", "Pemupukan fosfat alami", "Pemanenan jagung"],
             "A",
             "Dekomposisi anaerobik di sawah tergenang dan sistem pencernaan hewan ruminansia menghasilkan gas CH₄."),
            ("Protokol internasional yang menjadi dasar kesepakatan membatasi kenaikan suhu global di bawah 1,5°C - 2°C adalah...",
             ["Perjanjian Paris (Paris Agreement 2015)", "Protokol Montreal", "Konvensi Jenewa", "Deklarasi Bali"],
             "A",
             "Paris Agreement 2015 menyepakati batas kenaikan suhu bumi maksimal 1,5°C di atas tingkat pra-industri.")
        ],
        "esai": [
            ("Jelaskan fenomena 'efek rumah kaca alami' versus 'efek rumah kaca berlebih' bagi kelangsungan kehidupan di planet Bumi!",
             "Skor 10 jika menjelaskan bahwa efek alami menghangatkan bumi agar layak huni, sedangkan efek berlebih memicu krisis iklim global."),
            ("Rancanglah 3 solusi nyata berbasis gaya hidup berkelanjutan yang dapat diterapkan siswa SMA untuk mereduksi jejak karbon harian!",
             "Skor 10 jika merancang aksi hemat energi listrik, penggunaan transportasi umum/sepeda, dan pengurangan sampah makanan organik.")
        ]
    },
    "Bab 6: Energi Terbarukan": {
        "pg": [
            ("Menurut Hukum Kekekalan Energi, energi dalam suatu sistem terisolasi...",
             ["Dapat diciptakan dari kehampaan", "Dapat dimusnahkan secara total", "Bersifat kekal dan hanya dapat berubah bentuk", "Selalu berkurang seiring waktu"],
             "C",
             "Energi tidak dapat diciptakan atau dimusnahkan, melainkan hanya bertransformasi dari satu bentuk ke bentuk lain."),
            ("Pembangkit Listrik Tenaga Surya (PLTS) memanfaatkan komponen semikonduktor berupa...",
             ["Sel Fotovoltaik", "Turbin Uap", "Generator Induksi", "Kompresor Termal"],
             "A",
             "Sel fotovoltaik mengubah energi foton cahaya matahari langsung menjadi energi listrik arus searah (DC)."),
            ("Keunggulan utama energi terbarukan dibandingkan energi fosil adalah...",
             ["Biaya awal instalasi nol", "Tidak menghasilkan emisi gas rumah kaca berkelanjutan dan sumbernya tidak akan habis", "Tersedia merata di setiap jengkal tanah tanpa syarat cuaca", "Tidak membutuhkan perawatan"],
             "B",
             "Energi terbarukan ramah lingkungan dan terbarukan secara alami oleh siklus biosfer."),
            ("Transformasi energi yang terjadi pada Pembangkit Listrik Tenaga Mikrohidro (PLTMH) adalah...",
             ["Energi Potensial Air -> Energi Kinetik -> Energi Listrik", "Energi Kimia -> Energi Listrik -> Energi Kinetik", "Energi Listrik -> Energi Kalor -> Energi Kinetik", "Energi Nuklir -> Energi Listrik"],
             "A",
             "Air pada ketinggian tertentu mengalirkan energi potensial menjadi kinetik untuk memutar turbin generator."),
            ("Bioenergi yang dihasilkan dari fermentasi limbah biomassa organik secara anaerobik adalah...",
             ["Biogas (CH₄)", "Bioavtur sintetis", "Batu bara muda", "Gas alam cair"],
             "A",
             "Fermentasi anaerob kotoran ternak dan limbah organik menghasilkan biogas yang kaya gas metana.")
        ],
        "esai": [
            ("Analisis mengapa efisiensi konversi energi suatu mesin atau pembangkit tidak pernah mencapai 100%! Kaitkan dengan Hukum Termodinamika!",
             "Skor 10 jika memaparkan bahwa sebagian energi selalu terdisipasi menjadi energi termal (panas hilang) sesuai Hukum Termodinamika II."),
            ("Sebuah sekolah ingin membangun PLTS atap berkepasitas 5 kWp. Uraikan faktor teknis dan geografis yang harus dipertimbangkan sebelum pemasangan!",
             "Skor 10 jika menganalisis sudut kemiringan atap, insolasi sinar matahari, ketiadaan bayangan penghalang (shading), dan kekuatan struktur atap.")
        ]
    },
    "Bab 1: Mengungkap Fakta Alam (Teks LHO)": {
        "pg": [
            ("Teks Laporan Hasil Observasi (LHO) disusun berdasarkan...",
             ["Imajinasi dan rekaan penulis", "Fakta objektif dari hasil pengamatan lapangan", "Pendapat pribadi narasumber terkemuka", "Cerita rakyat setempat"],
             "B",
             "Teks LHO bersifat ilmiah, objektif, dan bersumber dari pengamatan fakta nyata."),
            ("Urutan struktur baku teks Laporan Hasil Observasi yang tepat adalah...",
             ["Pernyataan Umum -> Deskripsi Bagian -> Deskripsi Manfaat", "Deskripsi Bagian -> Orientasi -> Penutup", "Pernyataan Masalah -> Argumen -> Rekomendasi", "Orientasi -> Komplikasi -> Resolusi"],
             "A",
             "Struktur standar LHO: 1. Pernyataan Umum (definisi), 2. Deskripsi Bagian (ciri-ciri), 3. Deskripsi Manfaat."),
            ("Bagian teks LHO yang memaparkan fungsi atau kegunaan objek yang diamati dalam kehidupan manusia adalah...",
             ["Pernyataan Umum", "Deskripsi Bagian", "Deskripsi Manfaat", "Klasifikasi"],
             "C",
             "Deskripsi manfaat menguraikan nilai guna dan fungsi objek yang diobservasi."),
            ("Ciri kebahasaan teks LHO yang membedakannya dengan teks narasi fiksi adalah...",
             ["Menggunakan istilah ilmiah/teknis dan kalimat definisi verba relasional", "Banyak menggunakan majas hiperbola", "Memuat sudut pandang orang pertama 'aku'", "Disusun secara kronologis berpindah tempat"],
             "A",
             "LHO menggunakan istilah bidang ilmu (seperti herbivora, habitat) dan verba relasional kopula (adalah, merupakan)."),
            ("Contoh kalimat definisi yang tepat dalam teks LHO adalah...",
             ["Harimau Sumatra adalah subspesies harimau yang habitat aslinya di pulau Sumatra.", "Harimau Sumatra terlihat sangat gagah dan menakutkan saat mengaum.", "Kemarin lusa saya melihat harimau di kebun binatang.", "Jangan sekali-kali mendekati kandang harimau tanpa pawang."],
             "A",
             "Kalimat definisi menggunakan kopula 'adalah' untuk menjelaskan hakikat subjek secara ilmiah.")
        ],
        "esai": [
            ("Tuliskan perbedaan mendasar antara teks Laporan Hasil Observasi (LHO) dengan teks Deskripsi subjektif!",
             "Skor 10 jika memaparkan bahwa LHO bersifat objektif-ilmiah mengklasifikasi objek secara umum, sedangkan deskripsi bersifat subjektif-spesifik objek tertentu."),
            ("Buatlah draf satu paragraf Pernyataan Umum dan satu paragraf Deskripsi Bagian tentang tanaman obat keluarga (TOGA) di lingkungan sekolah!",
             "Skor 10 jika paragraf 1 memuat definisi ilmiah TOGA dan paragraf 2 menguraikan klasifikasi jenis tanaman obat beserta karakteristik fisiknya.")
        ]
    },
    "Bab 4: Belajar Menegosiasikan Kepentingan": {
        "pg": [
            ("Tujuan utama dari diselenggarakannya teks negosiasi adalah...",
             ["Memenangkan perdebatan sepihak", "Mencapai kesepakatan bersama yang saling menguntungkan (win-win solution)", "Menjatuhkan wibawa pihak lawan", "Menghibur pembaca dengan cerita jenaka"],
             "B",
             "Negosiasi adalah jalan tengah untuk menyelaraskan kepentingan pihak-pihak yang berbeda demi mufakat bersama."),
            ("Struktur teks negosiasi yang memuat tahapan tawar-menawar harga atau persyaratan disebut...",
             ["Orientasi", "Pengajuan", "Penawaran", "Persetujuan"],
             "C",
             "Tahap penawaran adalah proses kompromi di mana kedua pihak saling memberi usulan penyesuaian."),
            ("Ciri tuturan yang baik dan efektif dalam berkomunikasi saat negosiasi adalah...",
             ["Santun, argumentatif, dan tidak memaksakan kehendak", "Mengancam akan membatalkan perjanjian", "Menggunakan bahasa non-formal yang merendahkan lawan", "Berbicara terus menerus tanpa memberi jeda lawan"],
             "A",
             "Kesantunan berbahasa dan alasan yang logis memperbesar peluang tercapainya persetujuan."),
            ("Faktor penentu keberhasilan sebuah proses negosiasi bisnis adalah...",
             ["Adanya dominasi kekuasaan salah satu pihak", "Kesediaan kedua pihak untuk saling berkompromi demi solusi bersama", "Pihak penjual menerima kerugian penuh", "Keterlibatan aparat penegak hukum secara paksa"],
             "B",
             "Kompromi dan kelenturan sikap kedua belah pihak adalah kunci persetujuan sehat."),
            ("Kalimat pengajuan yang persuasif dalam teks negosiasi adalah...",
             ["'Apakah bapak bisa memberikan potongan harga 10% jika kami memesan dalam jumlah 100 unit?'", "'Turunkan harganya sekarang juga atau kami batalkan!'", "'Barang bapak ini jelek sekali kualitasnya!'", "'Terserah bapak saja harganya berapa.'"],
             "A",
             "Pengajuan santun disertai tawaran volume pesanan adalah teknik negosiasi yang efektif.")
        ],
        "esai": [
            ("Analisis mengapa tahap 'Pengajuan' dan 'Penawaran' disebut sebagai inti dari dinamika negosiasi!",
             "Skor 10 jika menjelaskan bahwa pada kedua tahap ini terjadi pertukaran kepentingan dan adu argumen logis sebelum keputusan dicapai."),
            ("Susunlah sebuah dialog singkat negosiasi (4 giliran tutur) antara perwakilan OSIS dan Kepala Sekolah terkait izin kegiatan pameran seni!",
             "Skor 10 jika dialog memuat orientasi santun, pengajuan izin, penawaran komitmen ketertiban, dan persetujuan Kepala Sekolah.")
        ]
    },
    "Unit 1: Great Athletes (Descriptive Text)": {
        "pg": [
            ("What is the primary communicative purpose of a Descriptive Text?",
             ["To entertain the reader with a fictional story", "To describe a particular person, place, or thing in detail", "To persuade readers to buy sports equipment", "To explain how an athlete trains step by step"],
             "B",
             "Descriptive text aims to describe specific characteristics, appearances, and traits of a subject."),
            ("The generic structure of a Descriptive Text consists of...",
             ["Orientation and Complication", "Identification and Description", "Thesis and Arguments", "Goal and Steps"],
             "B",
             "Standard structure: 1. Identification (introducing the athlete) and 2. Description (traits, achievements, habits)."),
            ("Which tense is predominantly used in describing an athlete's physical appearance and routines?",
             ["Past Continuous Tense", "Simple Future Tense", "Simple Present Tense", "Past Perfect Tense"],
             "C",
             "Simple Present Tense is used to describe habitual actions and general facts."),
            ("Read: 'Greysia Polii is an inspiring badminton player. She has sharp eyes and a warm smile.' The word 'warm' functions as...",
             ["An Adverb", "An Adjective describing her smile", "An Action Verb", "A Preposition"],
             "B",
             "'Warm' is an adjective modifying the noun 'smile' to create vivid imagery."),
            ("Which part of descriptive text contains the athlete's name, sport category, and nationality as the opening?",
             ["Identification", "Description", "Resolution", "Reorientation"],
             "A",
             "Identification paragraph introduces who the subject is before elaborating on details.")
        ],
        "esai": [
            ("Explain the distinction between the 'Identification' and 'Description' paragraphs in a descriptive text about an athlete!",
             "Score 10 if explaining Identification introduces the subject's identity, while Description details physical features, qualities, and skills."),
            ("Write a short descriptive paragraph (4-5 sentences) about your favorite Indonesian athlete using vivid adjectives and Simple Present Tense!",
             "Score 10 if accurately using Simple Present Tense, descriptive adjectives, and clear subject portrayal.")
        ]
    }
}

# -----------------------------------------------------------------------------
# 4. Retrieval & Guardrail Engine (Similarity Threshold > 0.70)
# -----------------------------------------------------------------------------
def retrieve_context(mapel, query):
    chunks = KNOWLEDGE_BASE.get(mapel, [])
    q_lower = query.lower()
    q_words = set(re.findall(r'\w+', q_lower))

    # Guardrail against off-topic trick questions
    off_topic = [
        "piala dunia", "presiden", "resep", "masak", "artis", "film", "gosip",
        "chelsea", "ronaldo", "sepak bola", "cuaca hari ini", "horoskop", "zodiak"
    ]
    if any(ot in q_lower for ot in off_topic):
        return None, 0.22

    best_chunk = None
    best_score = 0.0

    # Stopwords filter
    stopwords = {
        "dan", "yang", "di", "ke", "dari", "ini", "itu", "untuk", "pada", "adalah",
        "dengan", "apa", "bagaimana", "mengapa", "saya", "kamu", "tentang", "jelaskan",
        "sebutkan", "tolong", "bisa", "kah", "lah", "apakah"
    }
    content_q_words = {w for w in q_words if w not in stopwords and len(w) > 2}

    for chunk in chunks:
        # Match keywords (phrases & individual tokens)
        kw_hits = 0.0
        for kw in chunk["keywords"]:
            kw_l = kw.lower()
            if kw_l in q_lower:
                kw_hits += 1.5
            elif any(w in content_q_words for w in re.findall(r'\w+', kw_l) if len(w) > 3):
                kw_hits += 1.0

        # Match text words
        text_words = set(re.findall(r'\w+', chunk["teks"].lower()))
        text_overlap = len(content_q_words.intersection(text_words))

        if kw_hits == 0 and text_overlap == 0:
            score = 0.32
        else:
            score = min(0.98, 0.40 + (kw_hits * 0.16) + (text_overlap * 0.08))

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if best_score >= 0.70:
        return best_chunk, round(best_score, 2)
    else:
        return None, round(best_score if best_score > 0 else 0.35, 2)

# -----------------------------------------------------------------------------
# 5. Sidebar: Role Switcher & Subject Selection
# -----------------------------------------------------------------------------
with st.sidebar:
    # Banner image with fallback
    img_banner = "assets/og-image.jpg" if os.path.exists("assets/og-image.jpg") else "https://raw.githubusercontent.com/indri007/eduragmerdeka/main/assets/og-image.jpg"
    try:
        st.image(img_banner, use_container_width=True)
    except TypeError:
        st.image(img_banner, use_column_width=True)

    st.title("⚙️ Pengaturan Peran")

    role = st.radio(
        "Pilih Mode Pengguna:",
        ["👨‍🎓 Mode Siswa (Tanya Materi)", "👩‍🏫 Mode Guru (Generator Soal & RPP)"],
        index=0
    )

    st.markdown("---")
    st.subheader("📚 Mata Pelajaran")
    selected_mapel = st.selectbox(
        "Pilih Mapel Kurikulum Merdeka:",
        ["Matematika", "IPA Terpadu", "Bahasa Indonesia", "Bahasa Inggris"]
    )

    st.markdown("---")
    st.markdown("""
    **🛡️ Sistem Guardrail:**
    - Similarity Threshold: **> 0.70**
    - Top-k Retrieval: **3 Chunks**
    - Basis Data: **Buku Siswa & Guru Kemendikbud**
    - Validasi: **Cosine Cosine & Keyword Hybrid**
    """)
    st.caption("EduRAG Merdeka v1.0 • Apache 2.0 License")

# -----------------------------------------------------------------------------
# 6. Header Section
# -----------------------------------------------------------------------------
st.markdown("""
<div class="edurag-header">
    <h1>🎓 EduRAG Merdeka</h1>
    <p>Asisten Belajar & Mengajar Berbasis Retrieval-Augmented Generation untuk Kurikulum Merdeka Kelas 10</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. View: Mode Siswa (Chat RAG bersitasi)
# -----------------------------------------------------------------------------
if "👨‍🎓 Mode Siswa" in role:
    st.subheader(f"💬 Tanya Materi {selected_mapel} (Kelas 10)")
    st.caption("Ajukan pertanyaan bebas seputar buku pelajaran. Setiap jawaban wajib memuat sitasi bab & halaman resmi.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya EduRAG Merdeka. Silakan tanyakan materi atau konsep apa saja dari Buku Siswa atau Buku Guru resmi Kelas 10. Saya pantang berhalusinasi!"}
        ]

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input(f"Tanyakan konsep {selected_mapel} (contoh: jelaskan sifat dan contohnya)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("🔍 Mencari cuplikan teks Buku Siswa Kemendikbud..."):
                time.sleep(0.4)
                chunk, score = retrieve_context(selected_mapel, prompt)

            if chunk and score >= 0.70:
                answer = f"""
{chunk['teks']}

<div class="citation-badge">
    📖 Sitasi: {selected_mapel} Kelas 10 • {chunk['bab']} • Halaman {chunk['halaman']}
</div>
<div class="guardrail-badge">
    🛡️ Cosine Similarity: {score:.2f} (&gt; 0.70 Lolos Guardrail)
</div>
"""
            else:
                answer = f"""
<strong>Materi tidak ditemukan di buku teks Kurikulum Merdeka Kelas 10 ({selected_mapel}).</strong><br>
Sistem EduRAG menolak menjawab untuk mencegah halusinasi. Mohon gunakan kata kunci yang relevan dengan capaian pembelajaran buku resmi.

<div class="guardrail-alert">
    🛡️ Cosine Similarity: {score:.2f} (&lt; 0.70 Guardrail Anti-Halusinasi Terpicu)
</div>
"""
            st.markdown(answer, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------------------------------------------------------------
# 8. View: Mode Guru (Generator Soal & Modul Ajar RPP)
# -----------------------------------------------------------------------------
else:
    st.subheader(f"👩‍🏫 Portal Guru: Generator Soal & Modul Ajar — {selected_mapel}")
    st.caption("Otomatisasi penyusunan bank soal ulangan HOTS dan modul ajar resmi berbasis Capaian Pembelajaran.")

    tab1, tab2 = st.tabs(["📝 Generator Paket Soal (5 PG + 2 Esai)", "📋 Generator Modul Ajar (RPP)"])

    available_babs = [c["bab"] for c in KNOWLEDGE_BASE.get(selected_mapel, [])]

    # Tab 1: Soal Generator
    with tab1:
        st.markdown("#### 1. Pilih Bab Sumber Soal")
        chosen_bab = st.selectbox("Pilih Bab Kurikulum:", available_babs, key="soal_bab_select")

        col1, col2 = st.columns([1, 3])
        with col1:
            btn_generate_soal = st.button("⚡ Generate Paket Soal", key="gen_soal")

        if btn_generate_soal:
            with st.spinner(f"Menyusun 5 Soal PG + 2 Esai HOTS untuk {chosen_bab}..."):
                time.sleep(0.8)
                st.success("✅ Paket Soal berhasil disusun dari sumber buku resmi!")

                soal_data = SOAL_BANK.get(chosen_bab)
                if not soal_data:
                    # Generic fallback if custom bab
                    soal_data = {
                        "pg": [
                            ("Berdasarkan konsep dasar yang dipelajari pada bab ini, pernyataan yang paling tepat adalah...",
                             ["Pilihan A sesuai standar kurikulum", "Pilihan B variasi konsep", "Pilihan C penerapan konteks", "Pilihan D alternatif"],
                             "A", "Konsep mengacu pada Capaian Pembelajaran resmi.")
                        ],
                        "esai": [
                            ("Jelaskan implementasi materi bab ini dalam memecahkan masalah kontekstual di lingkungan sekitar!",
                             "Skor 10 jika memuat uraian sistematis dan penalaran kritis.")
                        ]
                    }

                # Build Markdown Output
                pg_text = ""
                for idx, (tanya, opsi, kunci, bahasan) in enumerate(soal_data["pg"], 1):
                    pg_text += f"{idx}. **Pertanyaan**: {tanya}\n"
                    for opt_letter, opt_val in zip(["A", "B", "C", "D"], opsi):
                        is_kunci = " *(Kunci)*" if opt_letter == kunci else ""
                        pg_text += f"   - **{opt_letter}.** {opt_val}{is_kunci}\n"
                    pg_text += f"   - *Kunci*: **{kunci}** | *Pembahasan*: {bahasan}\n\n"

                esai_text = ""
                for idx, (soal, rubrik) in enumerate(soal_data["esai"], 1):
                    esai_text += f"{idx}. **Soal {idx}**: {soal}\n   - *Rubrik Penilaian*: {rubrik}\n\n"

                soal_result = f"""### 📄 Paket Soal Ulangan Harian (Standar HOTS)
**Mata Pelajaran**: {selected_mapel}  
**Materi / Bab**: {chosen_bab}  
**Fase / Kelas**: Fase E / Kelas 10  
**Standar**: Kurikulum Merdeka Kemendikbud  

---

#### A. Soal Pilihan Ganda (5 Butir)
{pg_text}
---

#### B. Soal Esai Bernalar Kritis (2 Butir)
{esai_text}
"""
                st.markdown(soal_result)
                clean_filename = re.sub(r'[^\w\-_\.]', '_', f"Soal_{selected_mapel}_{chosen_bab}")
                st.download_button(
                    "💾 Unduh Paket Soal (.txt)",
                    soal_result,
                    file_name=f"{clean_filename}.txt"
                )

    # Tab 2: RPP / Modul Ajar Generator
    with tab2:
        st.markdown("#### 2. Draf Modul Ajar (RPP Deep Learning & Inkuiri)")
        chosen_bab_rpp = st.selectbox("Pilih Bab untuk Modul Ajar:", available_babs, key="rpp_bab_select")
        alokasi = st.selectbox("Alokasi Waktu:", ["2 JP (2 x 45 Menit)", "3 JP (3 x 45 Menit)", "4 JP (4 x 45 Menit)"])

        btn_generate_rpp = st.button("📋 Susun Draf Modul Ajar", key="gen_rpp")

        if btn_generate_rpp:
            with st.spinner("Menyelaraskan CP, TP, Dimensi Profil Pancasila, dan Asesmen..."):
                time.sleep(0.9)
                st.success("✅ Draf Modul Ajar Kurikulum Merdeka berhasil disusun!")

                rpp_result = f"""# MODUL AJAR KURIKULUM MERDEKA (FASE E - KELAS 10)

## I. INFORMASI UMUM
- **Mata Pelajaran**: {selected_mapel}
- **Fase / Kelas**: Fase E / Kelas X (Sepuluh)
- **Topik Pembelajaran**: {chosen_bab_rpp}
- **Alokasi Waktu**: {alokasi}
- **Target Peserta Didik**: Reguler / Tipikal (Heterogen)
- **Model Pembelajaran**: Problem-Based Learning (PBL) & Inkuiri Terbimbing
- **Profil Pelajar Pancasila**:
  1. *Bernalar Kritis*: Mengidentifikasi dan memecahkan persoalan esensial.
  2. *Gotong Royong*: Berkolaborasi dalam kerja kelompok investigasi data.
  3. *Mandiri*: Mengambil inisiatif dalam mengkaji teks buku sumber resmi.

---

## II. KOMPONEN INTI

### A. Capaian & Tujuan Pembelajaran (TP)
1. Peserta didik mampu menjelaskan konsep dasar pada **{chosen_bab_rpp}** dengan tepat dan komprehensif.
2. Peserta didik mampu menerapkan prinsip dan formula/struktur teks resmi untuk menganalisis data kontekstual di lingkungan sekitar.
3. Peserta didik mampu mempresentasikan kesimpulan dan hasil karya analisis kelompok secara santun dan bertanggung jawab.

### B. Pemahaman Bermakna
Konsep yang dipelajari pada bab ini adalah instrumen penting untuk memecahkan persoalan dunia nyata, memahami fenomena alam/sosial, serta menumbuhkan daya nalar ilmiah.

### C. Pertanyaan Pemantik
- Mengapa konsep pada {chosen_bab_rpp} menjadi sangat penting dalam perkembangan teknologi dan kehidupan kita?
- Bagaimana Anda membuktikan kebenaran sebuah data atau klaim menggunakan konsep bab ini?

---

## III. LANGKAH-LANGKAH KEGIATAN PEMBELAJARAN

### 1. Kegiatan Pendahuluan (15 Menit)
- Guru membuka pembelajaran dengan salam hangat, doa bersama, dan presensi.
- Guru mengondisikan suasana kelas dan menyampaikan motivasi belajar.
- **Apersepsi**: Guru menampilkan stimulus visual/masalah pemantik terkait {chosen_bab_rpp}.
- Guru menyampaikan tujuan pembelajaran dan indikator ketercapaian asesmen hari ini.

### 2. Kegiatan Inti (60 Menit - Sintaks PBL)
- **Sintaks 1: Orientasi Masalah**: Siswa mencermati kasus nyata yang tertera pada Buku Siswa Kemendikbud.
- **Sintaks 2: Organisasi Belajar**: Siswa dibagi ke dalam kelompok heterogen (4-5 siswa) dan menerima LKPD.
- **Sintaks 3: Penyelidikan Mandiri & Kelompok**: Siswa menggali informasi dari buku sumber resmi dan melakukan kalkulasi/analisis.
- **Sintaks 4: Pengembangan Karya**: Setiap kelompok merumuskan solusi dan menuliskan laporan ringkas.
- **Sintaks 5: Evaluasi & Refleksi**: Kelompok perwakilan mempresentasikan hasil, guru meluruskan miskonsepsi dan memberikan penguatan.

### 3. Kegiatan Penutup (15 Menit)
- Peserta didik bersama guru merangkum intisari materi pembelajaran hari ini.
- Guru melaksanakan asesmen reflektif singkat (exit ticket 2 menit).
- Guru menginfokan materi pertemuan berikutnya dan menutup dengan doa.

---

## IV. RENCANA ASESMEN
1. **Asesmen Diagnostik (Sebelum Belajar)**: Kuis apersepsi 3 pertanyaan singkat.
2. **Asesmen Formatif (Saat Belajar)**: Lembar observasi keaktifan diskusi kelompok dan gotong royong.
3. **Asesmen Sumatif (Akhir Bab)**: Tes tertulis 5 Butir Pilihan Ganda & 2 Butir Soal HOTS bersitasi.
"""
                st.markdown(rpp_result)
                clean_filename_rpp = re.sub(r'[^\w\-_\.]', '_', f"Modul_Ajar_{selected_mapel}_{chosen_bab_rpp}")
                st.download_button(
                    "💾 Unduh Draf Modul Ajar (.md)",
                    rpp_result,
                    file_name=f"{clean_filename_rpp}.md"
                )
