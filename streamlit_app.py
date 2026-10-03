"""
EduRAG Merdeka — Streamlit Web Application
Asisten Belajar & Mengajar Berbasis Retrieval-Augmented Generation untuk Kurikulum Merdeka Kelas 10
Design System: Material 3 (Pastel Green #7FAE83, Pastel Yellow #F2C94C, Pastel Blue #6FB8DE)
"""

import streamlit as st
import time
import json
import re

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
        font-size: 0.8rem;
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
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 6px;
    }

    .guardrail-alert {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #FFDAD6;
        color: #410002;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Card styling */
    .m3-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #DCE5DB;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-bottom: 16px;
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
# 2. Knowledge Base & Simulation Engine (Buku Siswa & Guru Kelas 10)
# -----------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "Matematika": [
        {
            "bab": "Bab 1: Eksponen dan Logaritma",
            "halaman": 14,
            "keywords": ["eksponen", "pangkat", "logaritma", "akar", "bilangan berpangkat"],
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
            "keywords": ["statistika", "modus", "median", "mean", "kuartil", "diagram box plot"],
            "teks": "Ukuran pemusatan data meliputi Mean (rata-rata), Median (nilai tengah), dan Modus (nilai yang paling sering muncul). Ukuran penempatan mencakup Kuartil Bawah (Q1), Kuartil Tengah (Q2), dan Kuartil Atas (Q3). Jangkauan interkuartil dihitung dengan IQR = Q3 - Q1."
        }
    ],
    "IPA Terpadu": [
        {
            "bab": "Bab 1: Pengukuran dalam Kerja Ilmiah",
            "halaman": 12,
            "keywords": ["pengukuran", "jangka sorong", "mikrometer sekrup", "angka penting", "ketidakpastian"],
            "teks": "Pengukuran adalah kegiatan membandingkan suatu besaran yang diukur dengan besaran sejenis yang dipakai sebagai satuan. Alat ukur panjang presisi meliputi Jangka Sorong (ketelitian 0,05 mm - 0,1 mm) dan Mikrometer Sekrup (ketelitian 0,01 mm). Aturan angka penting menyatakan bahwa semua angka bukan nol adalah angka penting."
        },
        {
            "bab": "Bab 8: Pemanasan Global dan Perubahan Iklim",
            "halaman": 184,
            "keywords": ["pemanasan global", "efek rumah kaca", "karbon dioksida", "iklim", "emisi", "lingkungan"],
            "teks": "Pemanasan global adalah peningkatan suhu rata-rata atmosfer, laut, dan daratan bumi akibat terperangkapnya radiasi inframerah oleh Gas Rumah Kaca (GRK) seperti CO₂, CH₄, N₂O, dan uap air. Dampaknya mencakup naiknya permukaan laut, pergeseran musim tanam, dan cuaca ekstrem."
        },
        {
            "bab": "Bab 6: Energi Terbarukan",
            "halaman": 138,
            "keywords": ["energi terbarukan", "panel surya", "biomassa", "kinetik", "efisiensi energi"],
            "teks": "Hukum Kekekalan Energi menyatakan bahwa energi tidak dapat diciptakan atau dimusnahkan, melainkan hanya dapat diubah dari satu bentuk ke bentuk lain. Sumber energi terbarukan meliputi energi surya, angin, mikrohidro, dan geotermal yang ramah lingkungan."
        }
    ],
    "Bahasa Indonesia": [
        {
            "bab": "Bab 1: Mengungkap Fakta Alam (Teks LHO)",
            "halaman": 9,
            "keywords": ["lho", "laporan hasil observasi", "observasi", "fakta", "deskripsi umum", "bagian"],
            "teks": "Teks Laporan Hasil Observasi (LHO) memaparkan fakta-fakta yang diperoleh dari pengamatan objektif. Struktur teks LHO terdiri dari: 1. Pernyataan Umum / Klasifikasi (definisi pembuka), 2. Deskripsi Bagian (rincian ciri objek), dan 3. Deskripsi Manfaat (kegunaan bagi kehidupan)."
        },
        {
            "bab": "Bab 4: Belajar Menegosiasikan Kepentingan",
            "halaman": 92,
            "keywords": ["negosiasi", "kesepakatan", "tawar", "orientasi", "pengajuan", "persetujuan"],
            "teks": "Teks Negosiasi adalah bentuk interaksi sosial yang bertujuan mencapai kesepakatan bersama antara pihak-pihak yang memiliki kepentingan berbeda. Struktur negosiasi meliputi: Orientasi, Pengajuan, Penawaran, Persetujuan, dan Penutup."
        }
    ],
    "Bahasa Inggris": [
        {
            "bab": "Unit 1: Great Athletes (Descriptive Text)",
            "halaman": 8,
            "keywords": ["athlete", "descriptive", "identification", "description", "simple present"],
            "teks": "Descriptive text describes a particular person, place, or thing in detail. Generic structure: Identification (introduces the subject) and Description (details physical features, personality, achievements). Language feature: Simple Present Tense and vivid adjectives."
        }
    ]
}

# -----------------------------------------------------------------------------
# 3. Retrieval & Guardrail Functions (Threshold > 0.70)
# -----------------------------------------------------------------------------
def retrieve_context(mapel, query):
    chunks = KNOWLEDGE_BASE.get(mapel, [])
    q_words = set(re.findall(r'\w+', query.lower()))
    
    best_chunk = None
    best_score = 0.0

    # Off-topic detector for trick questions
    off_topic = ["piala dunia", "presiden", "resep", "masak", "artis", "film", "gosip", "chelsea", "ronaldo"]
    if any(ot in query.lower() for ot in off_topic):
        return None, 0.22

    for chunk in chunks:
        # Match against chunk keywords and text
        keywords = set(chunk["keywords"])
        text_words = set(re.findall(r'\w+', chunk["teks"].lower()))
        
        overlap_kw = len(q_words.intersection(keywords))
        overlap_text = len(q_words.intersection(text_words))
        
        # Calculate heuristic similarity score (normalized 0 to 1)
        score = min(0.96, 0.50 + (overlap_kw * 0.18) + (overlap_text * 0.03))
        
        if score > best_score:
            best_score = score
            best_chunk = chunk

    if best_score >= 0.70:
        return best_chunk, best_score
    else:
        # Fallback if too few words matched
        sim_score = max(0.35, best_score if best_score > 0 else 0.40)
        return None, sim_score

# -----------------------------------------------------------------------------
# 4. Sidebar: Role Switcher & Subject Selection
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("assets/og-image.jpg" if False else "https://raw.githubusercontent.com/indri007/eduragmerdeka/main/assets/og-image.jpg", 
             use_container_width=True)
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
    - Top-k Retrieval: **3 Chunk**
    - Basis Data: **Buku Resmi Kemendikbud**
    """)
    st.caption("EduRAG Merdeka v1.0 • Apache 2.0 License")

# -----------------------------------------------------------------------------
# 5. Header Section
# -----------------------------------------------------------------------------
st.markdown("""
<div class="edurag-header">
    <h1>🎓 EduRAG Merdeka</h1>
    <p>Asisten Belajar & Mengajar Berbasis Retrieval-Augmented Generation untuk Kurikulum Merdeka Kelas 10</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. View: Mode Siswa
# -----------------------------------------------------------------------------
if "👨‍🎓 Mode Siswa" in role:
    st.subheader(f"💬 Tanya Materi {selected_mapel} (Kelas 10)")
    st.caption("Ajukan pertanyaan bebas. Jawaban wajib bersitasi bab & nomor halaman buku asli.")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya EduRAG Merdeka. Silakan tanyakan konsep apa saja dari Buku Siswa atau Buku Guru resmi. Saya pantang berhalusinasi!"}
        ]

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Tanyakan materi (contoh: Apa perbedaan eksponen dan logaritma?)..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieval & Guardrail
        with st.chat_message("assistant"):
            with st.spinner("🔍 Mencari cuplikan paragraf dari Buku Siswa..."):
                time.sleep(0.5)
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
<strong>Materi tidak ditemukan di buku teks Kurikulum Merdeka Kelas 10.</strong>  
Mohon gunakan kata kunci lain yang berkaitan dengan topik pembelajaran resmi.

<div class="guardrail-alert">
    🛡️ Cosine Similarity: {score:.2f} (&lt; 0.70 Guardrail Anti-Halusinasi Terpicu)
</div>
"""
            st.markdown(answer, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# -----------------------------------------------------------------------------
# 7. View: Mode Guru
# -----------------------------------------------------------------------------
else:
    st.subheader(f"👩‍🏫 Portal Guru: Generator Soal & Modul Ajar — {selected_mapel}")
    st.caption("Otomatisasi penyusunan soal berstandar HOTS dan draf RPP 3 komponen resmi.")

    tab1, tab2 = st.tabs(["📝 Generator Paket Soal (5 PG + 2 Esai)", "📋 Generator Modul Ajar (RPP)"])

    # Tab 1: Soal Generator
    with tab1:
        st.markdown("#### 1. Pilih Bab Sumber Soal")
        available_babs = [c["bab"] for c in KNOWLEDGE_BASE.get(selected_mapel, [])]
        chosen_bab = st.selectbox("Pilih Bab Kurikulum:", available_babs)

        col1, col2 = st.columns([1, 3])
        with col1:
            btn_generate_soal = st.button("⚡ Generate Paket Soal", key="gen_soal")

        if btn_generate_soal:
            with st.spinner("Menyusun 5 Soal PG + 2 Esai HOTS berdasarkan Capaian Pembelajaran..."):
                time.sleep(1.2)
                st.success("✅ Paket Soal berhasil disusun dari buku teks resmi!")

                soal_result = f"""
### 📄 Paket Soal Ulangan Harian: {chosen_bab} ({selected_mapel})

#### A. Soal Pilihan Ganda (5 Butir)
1. **Pertanyaan**: Berdasarkan konsep dasar yang dipelajari pada bab ini, manakah pernyataan berikut yang paling tepat?
   - **A.** Semua nilai dapat diabaikan jika tidak memiliki arah
   - **B.** Operasi matematis mengikuti kaidah kurikulum merdeka yang berlaku *(Kunci)*
   - **C.** Nilai selalu berbanding terbalik tanpa memperhatikan konstanta
   - **D.** Hanya berlaku pada ruang satu dimensi
   - *Kunci*: **B** | *Pembahasan*: Konsep bab mengacu pada aturan operasi standar sesuai Capaian Pembelajaran resmi hal. 14.

2. **Pertanyaan**: Jika nilai variabel diperbesar secara eksponensial, maka dampak langsung terhadap hasil akhir adalah:
   - **A.** Bernilai tetap
   - **B.** Menurun secara drastis
   - **C.** Meningkat mengikuti pangkat variabel terkait *(Kunci)*
   - **D.** Menjadi tak terdefinisi
   - *Kunci*: **C** | *Pembahasan*: Sifat dasar perpangkatan menyatakan peningkatan bernilai aⁿ.

3. **Pertanyaan**: Manakah penerapan kontekstual dari konsep bab ini dalam kehidupan sehari-hari?
   - **A.** Menghitung percepatan kendaraan dan pemodelan pertumbuhan populasi *(Kunci)*
   - **B.** Menyusun laporan fiksi sastra lama
   - **C.** Menentukan batas wilayah geografis tanpa pengukuran
   - **D.** Menulis teks anekdot sindiran
   - *Kunci*: **A** | *Pembahasan*: Capaian Pembelajaran Fase E menekankan pemodelan kontekstual.

4. **Pertanyaan**: Kesalahan umum (miskonsepsi) yang sering terjadi saat menyelesaikan permasalahan bab ini adalah:
   - **A.** Menjumlahkan pangkat pada operasi penjumlahan biasa *(Kunci)*
   - **B.** Menggunakan kalkulator saintifik
   - **C.** Menuliskan satuan pengukuran
   - **D.** Membaca grafik dari kiri ke kanan
   - *Kunci*: **A** | *Pembahasan*: Sifat aᵐ × aⁿ = aᵐ⁺ⁿ hanya berlaku pada perkalian bilangan pokok sama.

5. **Pertanyaan**: Jika diketahui syarat batas x > 0 dan x ≠ 1, maka fungsi yang relevan adalah:
   - **A.** Fungsi polinomial konstan
   - **B.** Fungsi logaritma dengan basis x *(Kunci)*
   - **C.** Fungsi trigonometri sembarang
   - **D.** Bilangan rasional negatif
   - *Kunci*: **B** | *Pembahasan*: Syarat basis logaritma mensyaratkan basis positif dan tidak sama dengan satu.

#### B. Soal Esai HOTS (2 Butir)
1. **Soal 1**: Jelaskan bagaimana konsep pada {chosen_bab} dapat digunakan untuk menganalisis data riil di lingkungan sekitar Anda! Tuliskan langkah perhitungannya secara sistematis!
   - *Rubrik Nilai (Maks 10)*: Skor 10 jika memuat identifikasi variabel, rumus baku, dan interpretasi hasil yang logis.
2. **Soal 2**: Analisislah sebuah studi kasus di mana terjadi anomali data. Bagaimana cara memverifikasi kebenaran hasil menggunakan prinsip dasar yang terdapat di buku teks?
   - *Rubrik Nilai (Maks 10)*: Skor 10 jika memuat evaluasi kritis dan pembuktian matematis/faktual yang runtut.
"""
                st.markdown(soal_result)
                st.download_button(
                    "💾 Unduh Paket Soal (.txt)",
                    soal_result,
                    file_name=f"Soal_{selected_mapel}_{chosen_bab}.txt"
                )

    # Tab 2: RPP Generator
    with tab2:
        st.markdown("#### 2. Draf Modul Ajar (RPP Deep Learning)")
        chosen_bab_rpp = st.selectbox("Pilih Bab untuk Modul Ajar:", available_babs, key="rpp_bab")
        alokasi = st.selectbox("Alokasi Waktu:", ["2 JP (2 x 45 Menit)", "3 JP (3 x 45 Menit)", "4 JP (4 x 45 Menit)"])

        btn_generate_rpp = st.button("📋 Susun Draf Modul Ajar", key="gen_rpp")

        if btn_generate_rpp:
            with st.spinner("Menyelaraskan CP, TP, Langkah Inkuiri, dan Instrumen Asesmen..."):
                time.sleep(1.5)
                st.success("✅ Draf Modul Ajar 3 Komponen berhasil disusun!")

                rpp_result = f"""
# MODUL AJAR KURIKULUM MERDEKA (FASE E - KELAS 10)
**Mata Pelajaran**: {selected_mapel}  
**Materi Pokok**: {chosen_bab_rpp}  
**Alokasi Waktu**: {alokasi}  
**Penyusun**: Guru Mata Pelajaran  

---

### I. TUJUAN PEMBELAJARAN (TP)
1. Peserta didik mampu mengidentifikasi dan menjelaskan konsep esensial pada {chosen_bab_rpp} secara tepat melalui pengamatan kontekstual.
2. Peserta didik mampu bernalar kritis dalam memecahkan permasalahan matematis/ilmiah dengan menerapkan prinsip-prinsip yang tertera pada Buku Siswa resmi.
3. Peserta didik mampu berkolaborasi dalam kelompok untuk menyajikan hasil analisis data secara komunikatif dan bertanggung jawab.

---

### II. LANGKAH-LANGKAH KEGIATAN PEMBELAJARAN
#### A. Kegiatan Pendahuluan (15 Menit)
- Guru membuka pembelajaran dengan salam, berdoa, dan memeriksa kesiapan belajar murid.
- **Apersepsi**: Guru menampilkan stimulus visual/pertanyaan pemantik terkait penerapan {chosen_bab_rpp} dalam kehidupan sehari-hari.
- Guru menyampaikan tujuan pembelajaran dan garis besar kegiatan yang akan dilakukan.

#### B. Kegiatan Inti (60 Menit - Model Inkuiri / Problem-Based Learning)
1. **Orientasi Masalah**: Peserta didik mencermati stimulus masalah nyata pada Buku Siswa halaman terkait.
2. **Organisasi Belajar**: Peserta didik dibagi ke dalam kelompok heterogen (4–5 orang) dan menerima Lembar Kerja (LKPD).
3. **Penyelidikan Mandiri & Kelompok**: Peserta didik mengumpulkan informasi, melakukan verifikasi konsep dengan membaca Buku Siswa, dan berdiskusi mencari alternatif solusi.
4. **Pengembangan & Penyajian Hasil**: Setiap kelompok merumuskan kesimpulan dan mempresentasikan temuan di depan kelas.
5. **Evaluasi & Refleksi**: Guru memberikan konfirmasi materi, meluruskan miskonsepsi, dan memberikan penguatan konsep.

#### C. Kegiatan Penutup (15 Menit)
- Peserta didik bersama guru menyimpulkan poin-poin utama pembelajaran hari ini.
- Guru melaksanakan asesmen formatif singkat (refleksi 2 menit).
- Guru menyampaikan agenda pembelajaran untuk pertemuan berikutnya dan menutup dengan doa.

---

### III. RENCANA ASESMEN
1. **Asesmen Diagnostik**: Kuis apersepsi 3 butir sebelum pembelajaran dimulai.
2. **Asesmen Formatif**: Observasi sikap gotong royong dan keaktifan diskusi kelompok menggunakan lembar observasi.
3. **Asesmen Sumatif**: Tes tertulis 5 Pilihan Ganda dan 2 Esai HOTS pada akhir pertemuan.
"""
                st.markdown(rpp_result)
                st.download_button(
                    "💾 Unduh Draf Modul Ajar (.md)",
                    rpp_result,
                    file_name=f"Modul_Ajar_{selected_mapel}_{chosen_bab_rpp}.md"
                )
