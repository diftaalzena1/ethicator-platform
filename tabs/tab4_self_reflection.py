# tabs/tab4_self_reflection.py
import streamlit as st
import os
import pandas as pd
from datetime import datetime
from utils import info_box, success_box, warning_box
from tabs.tab2_ethics_lab import load_models, load_resources, predict_labels

def run():
    """
    SELF REFLECTION — Awareness Mode & Personal Growth
    """
    # ==============================
    # 🌈 Styling Global
    # ==============================
    st.markdown("""
    <style>
    textarea { 
        color: #0A2342 !important;
        background-color: rgba(255,255,255,0.85) !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    label[for^="text_area"], label[for^="selectbox"] { 
        color: white !important;  /* WARNA LABEL PUTIH */
        font-weight: 600;
    }
    div.stButton > button {
        background-color: #0EA5E9;
        color: white;
        border-radius: 6px;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #0284C7;
        transform: scale(1.03);
    }
    </style>
    """, unsafe_allow_html=True)

    # ==============================
    # 🧱 Fungsi bantu render tabel
    # ==============================
    def render_styled_table(df, width="100%"):
        table_style = f"""
        <style>
        table {{
            width: {width};
            border-collapse: collapse;
        }}
        th {{
            text-align: center !important;
            padding: 8px;
            color: #142B45;
            font-weight: 600;
        }}
        td {{
            text-align: center !important;
            padding: 8px;
            color: #FFFFFF;
            font-weight: 500;
        }}
        thead tr {{
            background-color: #f2f2f2;
        }}
        </style>
        """
        st.markdown(table_style, unsafe_allow_html=True)
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    # ==============================
    # 🪞 Header
    # ==============================
    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <h1 style='color:#F8FAFC;'>🪞 Self Reflection</h1>
        <h3 style='color:#E0E0E0; font-weight:500;'>Refleksi Harian untuk Perilaku Online yang Lebih Bijak</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ==============================
    # ⚙️ Load Model & Resources
    # ==============================
    alay_dict_map, stopword_list, stemmer = load_resources()
    models, vectorizers = load_models()

    # ==============================
    # ✍️ Input Aktivitas Digital
    # ==============================
    st.subheader("✍️ Catat Aktivitas Digital Hari Ini")
    user_comment = st.text_area("Hari ini kamu sudah berkata/menulis apa di media sosial?")

    # ==============================
    # 😌 Refleksi Emosi & Perasaan
    # ==============================
    st.subheader("😌 Refleksi Emosi & Perasaan")

    # CSS: atur jarak antar elemen agar semua rapat
    st.markdown("""
    <style>
    h3 {
        margin-bottom: 0px !important;  /* jarak kecil antara subheader dan teks di bawahnya */
    }
    p.emotion-label {
        margin-top: 0px !important;
        margin-bottom: -8px !important;  /* rapat dengan selectbox */
    }
    div[data-baseweb="select"] {
        margin-top: -15px !important;
        padding-top: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Pilihan emosi
    emotion_options = ["😡 Marah", "😕 Bingung", "🙂 Senang", "😔 Sedih", "😐 Netral"]

    # Label putih
    st.markdown(
        '<p class="emotion-label" style="color:white; font-weight:50;">Bagaimana perasaanmu saat menulis/membalas komentar tadi?</p>',
        unsafe_allow_html=True
    )

    # Selectbox tanpa label bawaan
    user_emotion = st.selectbox(" ", emotion_options)

    # ==============================
    # ⚠️ Refleksi Kesalahan / Tantangan
    # ==============================
    st.subheader("⚠️ Refleksi Kesalahan atau Tantangan")
    user_mistake = st.text_area("Apakah ada momen hari ini kamu merasa kurang etis atau mendapat respons negatif?")

    # ==============================
    # 🌱 Tujuan Perbaikan Diri
    # ==============================
    st.subheader("🌱 Tujuan Perbaikan Diri")
    user_improvement = st.text_area("Apa yang akan kamu lakukan besok untuk lebih etis / empatik di dunia digital?")

    # ==============================
    # Simpan Aktivitas & Analisis
    # ==============================
    if st.button("💾 Analisis & Simpan Aktivitas"):
        if user_comment.strip():
            # Analisis komentar
            results = predict_labels(user_comment, models, vectorizers, alay_dict_map, stopword_list, stemmer)
            
            # Tentukan status utama & poin
            status, feedback, points = "🟢 Etis / Aman", "Komentar aman", 35
            any_red = any(r.get("Status", "") == "🔴 Hate Speech" for r in results.values())
            any_yellow = any(r.get("Status", "") == "🟡 Potensi Bias" for r in results.values())
            
            if any_red:
                status = "🔴 Hate Speech"
                feedback = "💡 Gunakan kata yang lebih sopan dan hindari nada menyerang."
                points = 10
            elif any_yellow:
                status = "🟡 Potensi Bias"
                feedback = "⚠️ Hati-hati dengan kata yang bisa menyinggung kelompok tertentu."
                points = 25

            # ==============================
            # Simpan ke CSV (aman untuk file kosong)
            # ==============================
            os.makedirs("data", exist_ok=True)
            log_path = "data/personal_ethics_log.csv"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row_dict = {
                "Tanggal": timestamp,
                "Komentar": user_comment,
                "Emosi": user_emotion,
                "Kesalahan/Tantangan": user_mistake,
                "Rencana Perbaikan": user_improvement,
                "Status Etika": status,
                "Feedback": feedback,
                "Poin": points
            }
            for label, info in results.items():
                row_dict[f"{label}_Prob"] = info.get("Probability", None)
                row_dict[f"{label}_Status"] = info.get("Status", None)
            
            new_row = pd.DataFrame([row_dict])

            # Aman baca CSV meskipun kosong
            if os.path.exists(log_path):
                try:
                    df_log = pd.read_csv(log_path)
                    df_log = pd.concat([df_log, new_row], ignore_index=True)
                except pd.errors.EmptyDataError:
                    df_log = new_row
            else:
                df_log = new_row

            df_log.to_csv(log_path, index=False, encoding='utf-8')

            # Update session state untuk Tab 5
            st.session_state["last_activity"] = new_row.iloc[0].to_dict()
            st.session_state["daily_points"] = points
            st.session_state["refresh_trigger"] = st.session_state.get("refresh_trigger", 0) + 1
            st.session_state["dashboard_refresh"] = st.session_state.get("dashboard_refresh", 0) + 1

            # Tampilkan hasil
            success_box(f"✅ Aktivitas berhasil disimpan! Status: {status}, Poin: {points} 🌿")

            # ==============================
            # 📋 Hasil Analisis Komentar
            # ==============================
            st.subheader("📋 Hasil Analisis Komentar")
            analysis_table = pd.DataFrame([
                {"Label": label, "Probability": round(info.get("Probability", 0), 2), "Status": info.get("Status", "")} 
                for label, info in results.items()
            ])
            render_styled_table(analysis_table)

        else:
            warning_box("⚠️ Silakan tulis sesuatu sebelum menyimpan.")

    # ==============================
    # 🪞 Aktivitas Terakhir (dari session jika ada)
    # ==============================
    if "last_activity" in st.session_state:
        activity = st.session_state["last_activity"]
        st.markdown(f"""
        <div style="
            margin-top: 15px;
            padding: 14px 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, rgba(19,78,74,0.6), rgba(102,153,255,0.4));
            color: #E0F2F1;
            font-style: italic;
            font-size: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        ">
        🪞 <b>Aktivitas terakhir kamu ({activity.get('Tanggal','-')}):</b><br>
        “{activity.get('Komentar','-')}”<br>
        Emosi: {activity.get('Emosi','-')}<br>
        Kesalahan/Tantangan: {activity.get('Kesalahan/Tantangan','-')}<br>
        Rencana Perbaikan: {activity.get('Rencana Perbaikan','-')}<br>
        Status Etika: {activity.get('Status Etika','-')}<br>
        Feedback: {activity.get('Feedback','-')}<br>
        Poin: {activity.get('Poin','-')}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # 💡 Keterangan Status Etika
    # ==============================
    st.subheader("💡 Keterangan Status Etika")
    df_status = pd.DataFrame([
        {"Status Etika": "🔴 Hate Speech", "Kapan Muncul": "Ada 1 kata/frasa kasar atau menyerang orang lain", "Intinya": "Sekali muncul → langsung dianggap Hate Speech"},
        {"Status Etika": "🟡 Potensi Bias", "Kapan Muncul": "Tidak ada Hate Speech, tapi ada kata/ungkapan yang bisa menyinggung kelompok tertentu", "Intinya": "Sekali muncul → dianggap Potensi Bias jika tidak ada Hate Speech"},
        {"Status Etika": "🟢 Etis / Aman", "Kapan Muncul": "Tidak ada Hate Speech maupun Potensi Bias", "Intinya": "Semua kata aman & sopan, komentar dianggap etis"},
    ])
    render_styled_table(df_status)
    
    st.markdown("---")

    # ==============================
    # 📘 Standar Penilaian Poin
    # ==============================
    st.subheader("📘 Standar Penilaian Poin")
    df_points = pd.DataFrame([
        {"Status Utama": "🔴 Hate Speech", "Deskripsi": "Komentar mengandung ujaran kebencian", "Poin": 10},
        {"Status Utama": "🟡 Potensi Bias", "Deskripsi": "Komentar ada potensi menyinggung tapi belum kasar", "Poin": 25},
        {"Status Utama": "🟢 Etis / Aman", "Deskripsi": "Komentar aman, positif, atau netral", "Poin": 35},
    ])
    render_styled_table(df_points)

    st.markdown("---")

    # ==============================
    # 💡 Info Box
    # ==============================
    info_box("""
    💡 Lihat Tab 5: <b>Ethics Dashboard</b> untuk memantau perkembangan etika digital, skor harian, dan refleksi mingguan secara interaktif.
    """)

    # ===== Navigasi =====
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        st.button("⬅️ Kembali ke Ethics Academy", on_click=lambda: st.session_state.update({'tab_selection':'Ethics Academy'}))
    with col2:
        st.button("➡️ Masuk ke Ethics Dashboard", on_click=lambda: st.session_state.update({'tab_selection':'Ethics Dashboard'}))
