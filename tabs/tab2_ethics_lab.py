# tabs/tab2_ethics_lab.py
import streamlit as st
import pandas as pd
from utils import load_models, load_resources, predict_labels, success_box

def run():
    """
    Halaman ETHICS LAB — Analisis Etika Komentar Digital
    Menyediakan input analisis komentar, hasil deteksi hate speech, dan rekomendasi etika digital.
    """

    # ==============================
    # Header Section
    # ==============================
    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <h1 style='color:#F8FAFC; font-size:34px; margin-bottom:10px;'>🧪 ETHICS LAB</h1>
        <h3 style='color:#e0e0e0; font-weight:500;'>Mendeteksi Nada & Etika, Meningkatkan Literasi Digital</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # Deskripsi Pembuka
    # ==============================
    st.markdown("""
    <div style='text-align:justify; color:#E2E8F0; font-size:15px;'>
    Analisis ini membantu mendeteksi apakah sebuah komentar mengandung  
    <b>ujaran kebencian (hate speech)</b> atau <b>bahasa kasar (abusive language)</b> —  
    agar kita bisa berkomunikasi lebih etis di ruang digital. 💬🤖
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # Load Model dan Resource
    # ==============================
    alay_dict_map, stopword_list, stemmer = load_resources()
    models, vectorizers = load_models()

    # ==============================
    # Gaya CSS Tabel Konsisten
    # ==============================
    table_style = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        text-align: center !important;
        padding: 8px;
        color: #142B45;  /* header biru */
        font-weight: 600;
    }
    td {
        text-align: center !important;
        padding: 8px;
        color: #FFFFFF; /* body teks putih */
        font-weight: 500;
    }
    thead tr {
        background-color: #f2f2f2;
    }
    </style>
    """
    st.markdown(table_style, unsafe_allow_html=True)

    # ==============================
    # Dataset Singkat & Sumber
    # ==============================
    with st.expander("ℹ️ Tentang Dataset dan Sumber", expanded=False):
        st.markdown("""
        <div style='text-align:justify; color:#CBD5E1; margin-bottom:15px;'>
        Model AI ini menggunakan dataset publik Kaggle untuk analisis komentar Indonesia:
        <ul>
            <li><b>ID Multi-Label Hate Speech & Abusive Twitter Text</b> – data.csv, abusive.csv, new_kamusalay.csv.  
                <i>Citation:</i> Okky Ibrohim & Indra Budi, 2019. Multi-label Hate Speech and Abusive Language Detection in Indonesian Twitter. In ALW3: 3rd Workshop on Abusive Language Online, 46-57.  
                <a href='https://www.kaggle.com/datasets/ilhamfp31/indonesian-abusive-and-hate-speech-twitter-text' target='_blank'>Kaggle</a>
            </li>
            <li><b>Indonesian Stoplist</b> – stopwordbahasa.csv.  
                <i>Citation:</i> Oswin Rahadiyan Hartono, 2014. Indonesian Stoplist (Bahasa Indonesia stop words dataset).  
                <a href='https://www.kaggle.com/datasets/oswinrh/indonesian-stoplist' target='_blank'>Kaggle</a>
            </li>
        </ul>
        </div>
        <br>
        """, unsafe_allow_html=True)

        # 📘 Kategori Utama
        st.markdown("### 📘 Kategori Utama")
        main_cat = pd.DataFrame({
            "Label": ["HS (Hate Speech)", "Abusive"],
            "Keterangan": [
                "Komentar mengandung ujaran kebencian atau penghinaan yang menargetkan seseorang atau kelompok tertentu.",
                "Komentar mengandung bahasa kasar, makian, atau pelecehan tanpa konteks kebencian tertentu."
            ]
        })
        st.markdown(main_cat.to_html(index=False, escape=False), unsafe_allow_html=True)

        # 🎯 Jenis Hate Speech
        st.markdown("### 🎯 Jenis Hate Speech")
        hs_cat = pd.DataFrame({
            "Label": [
                "HS_Individual", "HS_Group", "HS_Religion",
                "HS_Race", "HS_Physical", "HS_Gender", "HS_Other"
            ],
            "Keterangan": [
                "Ujaran kebencian yang ditujukan kepada individu tertentu.",
                "Ujaran kebencian yang ditujukan kepada kelompok sosial (suku, profesi, komunitas, dll).",
                "Berkaitan dengan agama atau kepercayaan.",
                "Berkaitan dengan ras atau etnis.",
                "Berkaitan dengan kondisi fisik atau disabilitas.",
                "Berkaitan dengan gender atau orientasi seksual.",
                "Hinaan umum, fitnah, atau ujaran kebencian lain yang tidak termasuk kategori di atas."
            ]
        })
        st.markdown(hs_cat.to_html(index=False, escape=False), unsafe_allow_html=True)

        # 🔥 Tingkat Intensitas
        st.markdown("### 🔥 Tingkat Intensitas")
        intensity = pd.DataFrame({
            "Label": ["HS_Weak", "HS_Moderate", "HS_Strong"],
            "Keterangan": [
                "Ujaran dengan nada ringan, seperti sindiran halus atau candaan yang berpotensi menyinggung.",
                "Ujaran dengan nada sedang, seperti kritik tajam atau sindiran keras.",
                "Ujaran dengan nada kuat, seperti makian langsung atau serangan verbal eksplisit."
            ]
        })
        st.markdown(intensity.to_html(index=False, escape=False), unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div style='text-align:justify; color:#CBD5E1;'>
        Satu komentar dapat memiliki <b>lebih dari satu label secara bersamaan</b>,  
        misalnya bersifat kasar (Abusive) <i>sekaligus</i> menyerang kelompok tertentu (HS_Group).
        </div>
        """, unsafe_allow_html=True)

    # ==============================
    # Input Komentar
    # ==============================
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.04);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        margin-top: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    ">
        <h4 style='color:#F8FAFC; margin-bottom:8px;'>💬 Masukkan Komentar untuk Analisis Etika Digital</h4>
        <p style='color:#CBD5E1; font-size:15px; text-align:justify;'>
            Ketik komentar, opini, atau pesan yang ingin kamu analisis menggunakan model AI.  
            Sistem akan memeriksa potensi ujaran kebencian dan bahasa kasar secara otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Text area
    user_input = st.text_area(" ", placeholder="Contoh: Aku benci banget sama orang kayak gitu!", height=140)

    # Tombol submit
    submit_btn = st.button("📤 Analisis Komentar")

    # Proses hanya jika tombol ditekan
    if submit_btn and user_input:
        results = predict_labels(user_input, models, vectorizers, alay_dict_map, stopword_list, stemmer)
        df = pd.DataFrame(results).T.reset_index().rename(columns={'index': 'Label'})

        # ==============================
        # Hasil Analisis
        # ==============================
        st.subheader("📋 Hasil Analisis Komentar")
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

        # Panduan Membaca
        with st.expander("📘 Cara Membaca Hasil"):
            st.markdown("""
            <div style='text-align:justify; color:#E2E8F0;'>
            Hasil di atas menunjukkan kategori ujaran kebencian (HS) dan bahasa kasar (Abusive)  
            yang terdeteksi dari komentar kamu.
            </div>

            <br>

            | Label | Arti |
            |:-------|:-----|
            | 🔴 Hate Speech | Komentar mengandung ujaran kebencian yang menyerang individu atau kelompok. |
            | 🟡 Potensi Bias | Komentar mengandung kata yang berpotensi menyinggung kelompok tertentu. |
            | 🟢 Etis / Aman | Tidak ditemukan ujaran kebencian maupun bahasa kasar. |

            <br>

            <div style='text-align:justify; color:#E2E8F0;'>
            <b>Contoh Interpretasi:</b><br>
            - <code>HS_Group 🔴</code> → Menyerang kelompok berdasarkan etnis, agama, atau profesi. <br>
            - <code>Abusive 🔴</code> → Mengandung kata kasar atau makian langsung. <br>
            - <code>HS_Weak 🟡</code> → Nada sindiran atau ejekan ringan. <br>
            - <code>HS_None 🟢</code> → Komentar aman, tidak ditemukan ujaran kebencian.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ==============================
        # Rekomendasi Etika Digital
        # ==============================
        feedback = []
        for r in results.values():
            status = r.get("Status", "")
            if status == "🔴 Hate Speech":
                feedback.append("💡 Gunakan kata yang lebih sopan dan hindari nada menyerang.")
            elif status == "🟡 Potensi Bias":
                feedback.append("⚠️ Hati-hati dengan kata yang bisa menyinggung kelompok tertentu.")

        unique_feedback = list(set(feedback))

        if unique_feedback:
            st.markdown("### 💬 Rekomendasi Etika Digital")
            for msg in unique_feedback:
                st.markdown(f"""
                <div style="
                    background-color: rgba(255,255,255,0.04);
                    border-left: 5px solid #38BDF8;
                    border-radius: 8px;
                    padding: 12px 15px;
                    margin-bottom: 10px;
                    font-size: 15px;
                    text-align: justify;
                    color: #E0E7FF;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    {msg}
                </div>
                """, unsafe_allow_html=True)
        else:
            success_box("✅ Komentar aman — tidak terdeteksi ujaran kebencian atau bahasa kasar.")

        # ==============================
        # Catatan Penutup
        # ==============================
        st.markdown("""
        ---
        <div style='text-align: justify; color: #E0E7FF; font-style: italic;'>
        🌱 Etika digital bukan soal siapa yang paling benar,  
        tetapi tentang bagaimana kita saling menghargai dalam percakapan online.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


    # ===== Navigasi =====
    col1,col2=st.columns(2)
    with col1:
        st.button("⬅️ Kembali ke Welcome Hub", on_click=lambda: st.session_state.update({'tab_selection':'Welcome Hub'}))
    with col2:
        st.button("➡️ Masuk ke Ethics Academy", on_click=lambda: st.session_state.update({'tab_selection':'Ethics Academy'}))