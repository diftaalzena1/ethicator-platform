# ============================================================
# 📚 tab3_ethics_academy.py — Ethics Academy (Daily Random Quiz)
# ============================================================
import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from utils import success_box, warning_box
import matplotlib.pyplot as plt
import plotly.graph_objs as go

SCORE_LOG_PATH = "data/personal_scores.csv"

# ============================================================
# 🔧 Fungsi logging skor harian
# ============================================================
def log_score(total_score):
    today_str = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([[today_str, total_score]], columns=["Tanggal","Total_Skor"])
    if os.path.exists(SCORE_LOG_PATH):
        df_existing = pd.read_csv(SCORE_LOG_PATH)
        df_existing = df_existing[df_existing["Tanggal"] != today_str]
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(SCORE_LOG_PATH, index=False)

# ============================================================
# 🚀 Fungsi utama tab
# ============================================================
def run():
    # ===== Styling =====
    st.markdown("""
    <style>
    .stRadio label, .stRadio div { color: #F8FAFC !important; }
    div.stButton > button { background-color: #0EA5E9; color: white; border-radius:6px; font-weight:600;}
    div.stButton > button:hover { background-color:#0284C7; transform:scale(1.03);}
    </style>
    """, unsafe_allow_html=True)

    # ===== Header & Quote =====
    st.markdown("<h1 style='color:#F8FAFC;text-align:center;'>🎓 Ethics Academy</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#E0E0E0;text-align:center;font-weight:500;'>Belajar Etika, Tumbuh Bersama</h3>", unsafe_allow_html=True)
    st.markdown("---")

    quotes = [
        "💭 Etika digital dimulai dari cara kita menulis komentar.",
        "💭 Berempati di dunia maya sama pentingnya dengan di dunia nyata.",
        "💭 Setiap komentar positif membantu membangun komunitas online yang sehat.",
        "💭 Menghindari debat panas di internet adalah bentuk kecerdasan emosional.",
        "💭 Kata-kata baik bisa menjadi algoritma kebaikan di ruang digital."
    ]
    if "quote_index" not in st.session_state:
        st.session_state.quote_index = random.randint(0,len(quotes)-1)
    st.markdown(f"<div style='background:linear-gradient(135deg,rgba(19,78,74,0.9),rgba(102,153,255,0.6));padding:14px 18px;border-radius:10px;color:white;text-align:center;font-size:16px;'>{quotes[st.session_state.quote_index]}</div>", unsafe_allow_html=True)

    # ===== Tips Etika =====
    st.markdown("---")
    st.subheader("💎 Rangkuman Tips Etika Digital")
    tips=[]
    tips_path="data/tips.csv"
    if os.path.exists(tips_path):
        try:
            tips = pd.read_csv(tips_path,header=None,encoding="utf-8")[0].tolist()
        except Exception as e:
            warning_box(f"⚠️ Gagal membaca tips.csv: {e}")
    else:
        warning_box("⚠️ File tips.csv tidak ditemukan.")

    categories=["Berempati","Hindari Konflik","Verifikasi Fakta"]
    for cat in categories:
        with st.expander(f"💡 Tips {cat}", expanded=False):
            if tips:
                key=f"tip_{cat}"
                if key not in st.session_state: st.session_state[key]=random.choice(tips)
                st.markdown(f"<div style='background:linear-gradient(135deg,rgba(19,78,74,0.9),rgba(102,153,255,0.5));padding:10px 14px;border-radius:8px;color:white;font-size:14px;'>{st.session_state[key]}</div>", unsafe_allow_html=True)

    if st.button("🔄 Lihat Tips Lain"):
        for cat in categories: st.session_state[f"tip_{cat}"]=random.choice(tips) if tips else ""
        st.session_state.quote_index=random.randint(0,len(quotes)-1)
        st.session_state["_rerun"]=random.random()

    # ===== Tombol Mulai =====
    st.markdown("---")
    st.subheader("🎮 Mini-Game & 🧩 Kuis Etika Digital")
    if "started" not in st.session_state: st.session_state.started=False
    if not st.session_state.started:
        if st.button("▶️ Mulai Game & Kuis"):
            st.session_state.started=True
            st.session_state.selected_answers={}
            st.session_state.quiz_score=0
            st.session_state.game_score=0
    else:
        # ===== Seed harian untuk random =====
        today_str = datetime.now().strftime("%Y-%m-%d")
        random.seed(today_str)

        # ===== Mini-Game =====
        mini_game_scenarios=[
            ("Teman menulis komentar kasar di postinganmu", ["Balas dengan kata kasar","Senyapkan & beri saran sopan","Balas dengan meme lucu"],1),
            ("Orang asing mengkritik ide kamu secara tajam", ["Menghina balik","Abaikan & respon sopan","Laporkan ke moderator"],1),
            ("Ada debat panas di kolom komentar", ["Ikut memanas","Berikan fakta & argumen sopan","Salahkan semua pihak"],1)
        ]

        if "shuffled_mini_game" not in st.session_state or st.session_state.get("game_day") != today_str:
            temp = mini_game_scenarios.copy()
            random.shuffle(temp)
            for i in range(len(temp)):
                options = temp[i][1].copy()
                random.shuffle(options)
                temp[i] = (temp[i][0], options, options.index(temp[i][1][temp[i][2]]))
            st.session_state.shuffled_mini_game = temp
            st.session_state.game_day = today_str

        mini_game_scenarios = st.session_state.shuffled_mini_game

        st.markdown("### Mini-Game: Pilih cara membalas komentar negatif")
        for i,(scenario, options, correct_idx) in enumerate(mini_game_scenarios):
            st.markdown(f"**Skenario {i+1}: {scenario}**")
            choice=st.radio("",options,key=f"game_{i}")
            st.session_state.selected_answers[f"game_{i}"]=choice

        # ===== Kuis =====
        empathetic_quiz=[
            ("Komentar yang menghargai pendapat orang lain","Komentar yang menegur dengan kasar",0),
            ("Menanyakan kabar teman dengan sopan","Mengabaikan teman yang meminta bantuan",0),
            ("Memberikan saran dengan lembut","Menghina ide orang lain secara terbuka",0)
        ]

        if "shuffled_quiz" not in st.session_state or st.session_state.get("quiz_day") != today_str:
            temp = empathetic_quiz.copy()
            random.shuffle(temp)
            st.session_state.shuffled_quiz = temp
            st.session_state.quiz_day = today_str

        empathetic_quiz = st.session_state.shuffled_quiz

        st.markdown("### Kuis: Mana yang lebih berempati?")
        for i,(opt1,opt2,correct) in enumerate(empathetic_quiz):
            st.markdown(f"**Q{i+1}: Pilih yang lebih berempati**")
            ans=st.radio("",(opt1,opt2),key=f"quiz_{i}")
            st.session_state.selected_answers[f"quiz_{i}"]=ans

        # ===== Tombol Kumpulkan =====
        if st.button("📥 Kumpulkan Jawaban"):
            st.session_state.game_score=0
            for i,(s,opt,correct_idx) in enumerate(mini_game_scenarios):
                ans=st.session_state.selected_answers.get(f"game_{i}")
                if ans==opt[correct_idx]: st.session_state.game_score+=1

            st.session_state.quiz_score=0
            for i,(opt1,opt2,correct) in enumerate(empathetic_quiz):
                ans=st.session_state.selected_answers.get(f"quiz_{i}")
                if ans==opt1: st.session_state.quiz_score+=1

            total_score=st.session_state.game_score+st.session_state.quiz_score
            log_score(total_score)

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(19,78,74,0.9),rgba(102,153,255,0.6));padding:15px;border-radius:10px;color:white;font-weight:600;text-align:center;font-size:16px;' >
                <p>Skor Mini-Game<br>{st.session_state.game_score}/{len(mini_game_scenarios)}</p>
                <p>Skor Kuis Empati<br>{st.session_state.quiz_score}/{len(empathetic_quiz)}</p>
                <p>Skor Total Hari Ini<br>{total_score} pts</p>
            </div><br>
            """ , unsafe_allow_html=True)

            if total_score>=5:
                st.markdown("<p style='color:white;font-weight:500;'>🌟 Hebat! Kamu menunjukkan etika digital yang baik hari ini.</p>", unsafe_allow_html=True)
            elif total_score>=3:
                st.markdown("<p style='color:white;font-weight:500;'>🙂 Bagus, tapi masih ada ruang untuk lebih berempati.</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:white;font-weight:500;'>⚠️ Ayo tingkatkan etika digitalmu, perhatikan kata-kata dan sikapmu!</p>", unsafe_allow_html=True)

            # ===== Jawaban dengan card-style =====
            st.markdown("### 📝 Jawaban Kamu")

            st.markdown("#### Mini-Game")
            for key, val in st.session_state.selected_answers.items():
                if key.startswith("game_"):
                    idx=int(key.split("_")[1])
                    correct_opt=mini_game_scenarios[idx][1][mini_game_scenarios[idx][2]]
                    is_correct = val==correct_opt
                    color="#28A745" if is_correct else "#DC3545"
                    st.markdown(f"""
                    <div style="
                        background-color: #1B3B5C;
                        padding:10px 12px;
                        border-left:5px solid {color};
                        border-radius:6px;
                        margin-bottom:6px;
                        color:white;
                        font-weight:500;
                        ">
                        <b>Skenario {idx+1}:</b> {val} {'✅' if is_correct else '❌'}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("#### Kuis Empati")
            for key, val in st.session_state.selected_answers.items():
                if key.startswith("quiz_"):
                    idx=int(key.split("_")[1])
                    correct_opt=empathetic_quiz[idx][0]
                    is_correct = val==correct_opt
                    color="#28A745" if is_correct else "#DC3545"
                    st.markdown(f"""
                    <div style="
                        background-color: #1B3B5C;
                        padding:10px 12px;
                        border-left:5px solid {color};
                        border-radius:6px;
                        margin-bottom:6px;
                        color:white;
                        font-weight:500;
                        ">
                        <b>Q{idx+1}:</b> {val} {'✅' if is_correct else '❌'}
                    </div>
                    """, unsafe_allow_html=True)

    # ===== Reset Skor =====
    st.markdown("---")
    st.subheader("♻️ Reset Skor Hari Ini")
    def reset_scores():
        st.session_state.started=False
        st.session_state.selected_answers={}
        st.session_state.game_score=0
        st.session_state.quiz_score=0
        if os.path.exists(SCORE_LOG_PATH):
            df=pd.read_csv(SCORE_LOG_PATH)
            today=datetime.now().strftime("%Y-%m-%d")
            df=df[df["Tanggal"]!=today]
            df.to_csv(SCORE_LOG_PATH,index=False)
        success_box("🔄 Skor & jawaban telah di-reset!")

    st.button("Reset Skor", on_click=reset_scores)

    # ===== Grafik Skor Harian =====
    st.markdown("---")
    st.subheader("📈 Grafik Progres Skor Harian (7 Hari Terakhir)")

    if os.path.exists(SCORE_LOG_PATH):
        df_score = pd.read_csv(SCORE_LOG_PATH)
        df_score["Tanggal"] = pd.to_datetime(df_score["Tanggal"])
        df_score["Total_Skor"] = df_score["Total_Skor"].astype(int)
        daily_df = df_score.groupby("Tanggal")["Total_Skor"].sum().reset_index().sort_values("Tanggal").tail(7)

        if not daily_df.empty:
            x_labels = daily_df["Tanggal"].dt.date.astype(str).tolist()
            y_values = daily_df["Total_Skor"].tolist()

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_labels,
                y=y_values,
                mode='lines+markers+text',
                line=dict(color='#F8FAFC', width=2),
                marker=dict(size=8, color='#F8FAFC'),
                text=y_values,
                textposition="top center",
                textfont=dict(size=10, color='white'),
                hovertemplate='Tanggal: %{x}<br>Skor: %{y}<extra></extra>'
            ))

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=40, t=20, b=40),
                xaxis=dict(title=dict(text="Tanggal", font=dict(color='white'), standoff=60),
                           type='category', tickangle=45, tickfont=dict(color='white'), showgrid=False),
                yaxis=dict(title=dict(text="Skor", font=dict(color='white'), standoff=30),
                           tickmode='linear', dtick=1, tickfont=dict(color='white'), showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("<p style='color:white;'>Tidak ada data skor harian untuk ditampilkan.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:white;'>Belum ada skor harian yang tersimpan.</p>", unsafe_allow_html=True)

    # ===== Navigasi =====
    st.markdown("---")
    col1,col2=st.columns(2)
    with col1:
        st.button("⬅️ Kembali ke Ethics Lab", on_click=lambda: st.session_state.update({'tab_selection':'Ethics Lab'}))
    with col2:
        st.button("➡️ Masuk ke Self Reflection", on_click=lambda: st.session_state.update({'tab_selection':'Self Reflection'}))
