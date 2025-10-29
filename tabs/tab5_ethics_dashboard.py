# ============================================================
# 📊 tab5_ethics_dashboard.py — Versi tanpa Badge Historis
# ============================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import os
from datetime import datetime, timedelta
from utils import info_box
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 🔧 Fungsi: Render tabel dengan styling HTML custom
# ============================================================
def render_styled_table(df: pd.DataFrame):
    table_style = """
    <style>
    table { width: 100%; border-collapse: collapse; }
    th { text-align: center !important; padding: 8px; color: #142B45; font-weight: 600; }
    td { text-align: center !important; padding: 8px; color: #FFFFFF; font-weight: 500; }
    thead tr { background-color: #f2f2f2; }
    </style>
    """
    st.markdown(table_style, unsafe_allow_html=True)
    st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)


# ============================================================
# 🧩 Helper: styled metric card (HTML)
# ============================================================
def module_card(title: str, value: str, subtitle: str = "", bg_color: str = "#0EA5E9"):
    html = f"""
    <div style="
        background: linear-gradient(135deg, {bg_color} 0%, rgba(255,255,255,0.02) 100%);
        color: #FFFFFF;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        text-align: left;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    ">
        <div style="font-size:14px; opacity:0.9; font-weight:600;">{title}</div>
        <div style="font-size:28px; font-weight:700; margin-top:6px;">{value}</div>
        <div style="font-size:12px; opacity:0.85; margin-top:6px;">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# 🚀 Fungsi utama dashboard
# ============================================================
def run():
    # ============================================================
    # 🏷️ Header
    # ============================================================
    st.markdown("""
    <div style='text-align:center; margin-bottom:18px;'>
        <h1 style='color:#F8FAFC; margin-bottom:6px;'>🖥️ Ethics Dashboard</h1>
        <h3 style='color:#E0E0E0; font-weight:500; margin-top:0px;'>
            🌿 Cermin Data untuk Menumbuhkan Empati dan Etika di Dunia Digital
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # ============================================================
    # 📥 Load personal ethics log
    # ============================================================
    log_path = "data/personal_ethics_log.csv"
    if not os.path.exists(log_path):
        st.warning("⚠️ Belum ada data personal ethics log. Tambahkan melalui Tab Self Reflection.")
        return

    try:
        df = pd.read_csv(log_path)
    except Exception as e:
        st.error(f"Gagal membaca log: {e}")
        return

    if df.empty:
        st.info("Belum ada data aktivitas yang tersimpan.")
        return

    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce").dt.date
    df = df.dropna(subset=["Tanggal"])

    # ============================================================
    # 📊 Summary Metrics
    # ============================================================
    today = datetime.now().date()
    start_7d = today - timedelta(days=6)
    df_today = df[df["Tanggal"] == today]
    df_week = df[(df["Tanggal"] >= start_7d) & (df["Tanggal"] <= today)]

    total_comments = len(df)
    daily_points = int(df_today["Poin"].sum()) if not df_today.empty else 0
    weekly_points = int(df_week["Poin"].sum()) if not df_week.empty else 0

    pos_comments = len(df[df["Status Etika"].str.contains("🟢", na=False)])
    bias_comments = len(df[df["Status Etika"].str.contains("🟡", na=False)])
    hate_comments = len(df[df["Status Etika"].str.contains("🔴", na=False)])

    pct_safe = (pos_comments / total_comments * 100) if total_comments else 0
    pct_bias = (bias_comments / total_comments * 100) if total_comments else 0
    pct_hate = (hate_comments / total_comments * 100) if total_comments else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        module_card("🔥 Poin Hari Ini", f"{daily_points}", "Total poin hari ini", "#10B981")
        module_card("📅 Poin Minggu Ini", f"{weekly_points}", "Akumulasi 7 hari", "#0EA5E9")
    with c2:
        module_card("💬 Total Komentar", f"{total_comments}", "Komentar tercatat", "#6366F1")
        module_card("💚 Etis / Aman", f"{pct_safe:.1f}%", "Persentase komentar etis", "#22C55E")
    with c3:
        module_card("💛 Potensi Bias", f"{pct_bias:.1f}%", "Komentar berpotensi bias", "#F59E0B")
        module_card("❤️ Hate Speech", f"{pct_hate:.1f}%", "Komentar berisiko tinggi", "#EF4444")

    st.markdown("---")

    # ============================================================
    # 💡 Insight Otomatis
    # ============================================================
    # Hitung perubahan poin dibanding kemarin
    yesterday = today - timedelta(days=1)
    df_yesterday = df[df["Tanggal"] == yesterday]
    yesterday_points = int(df_yesterday["Poin"].sum()) if not df_yesterday.empty else 0

    diff_points = daily_points - yesterday_points

    if diff_points > 0:
        insight_text = f"📈 Skor meningkat {diff_points:.1f} poin dibanding kemarin — pertahankan semangat positif!"
        color = "#22C55E"  # hijau
    elif diff_points < 0:
        insight_text = f"📉 Skor menurun {abs(diff_points):.1f} poin dibanding kemarin — evaluasi penyebabnya dengan tenang."
        color = "#F59E0B"  # kuning
    else:
        insight_text = "⚖️ Skor stabil dibanding kemarin — konsisten tetap baik!"
        color = "#60A5FA"  # biru

    st.markdown(
        f"<p style='color:{color}; font-size:16px; font-weight:500;'>{insight_text}</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # ============================================================
    # 📝 10 Aktivitas Terakhir
    # ============================================================
    st.subheader("📝 10 Aktivitas Terakhir")

    df["Tanggal"] = pd.to_datetime(df["Tanggal"], dayfirst=True, errors="coerce").dt.date
    df = df.dropna(subset=["Tanggal"])
    df_recent = df.sort_values(by="Tanggal", ascending=True).tail(10)

    df_recent = df_recent[[
        "Tanggal",
        "Komentar",
        "Emosi",
        "Kesalahan/Tantangan",
        "Rencana Perbaikan",
        "Status Etika",
        "Feedback",
        "Poin"
    ]].rename(columns={"Emosi": "Emosi (reflektif)"})

    render_styled_table(df_recent)
    st.markdown("---")

    # ============================================================
    # 📉 Distribusi Emosi
    # ============================================================
    st.subheader("📉 Distribusi Emosi")
    if "Emosi" in df.columns and not df["Emosi"].dropna().empty:
        emo_counts = df["Emosi"].value_counts().reset_index()
        emo_counts.columns = ["Emosi", "Frekuensi"]
        emotion_color_map = {
            "😡 Marah": "#EF4444",
            "😕 Bingung": "#F59E0B",
            "🙂 Senang": "#10B981",
            "😔 Sedih": "#60A5FA",
            "😐 Netral": "#6366F1"
        }
        colors = [emotion_color_map.get(e, "#94A3B8") for e in emo_counts["Emosi"]]
        fig = px.bar(emo_counts, x="Emosi", y="Frekuensi", color=emo_counts["Emosi"],
                     color_discrete_sequence=colors, text="Frekuensi")
        fig.update_traces(showlegend=False, marker_line_width=0)
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="white"),
            yaxis=dict(color="white", dtick=1, tickmode="linear")
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data emosi untuk divisualisasikan.")
    st.markdown("---")

    # ============================================================
    # ☁️ Analisis Bahasa Digital
    # ============================================================
    st.subheader("☁️ Analisis Bahasa Digital")
    corpus = " ".join(df["Komentar"].dropna().astype(str))
    words = [w.lower() for w in corpus.split() if len(w) > 2]
    counter = Counter(words)
    top_words = counter.most_common(15)

    col_a, col_b = st.columns(2)
    with col_a:
        if top_words:
            top_df = pd.DataFrame(top_words, columns=["word", "count"]).sort_values("count", ascending=True)
            fig = px.bar(top_df, x="count", y="word", orientation="h")
            fig.update_xaxes(tickmode="linear", dtick=1)
            fig.update_traces(marker=dict(color=top_df["count"], colorscale=[[0, "#0EA5E9"], [1, "#6366F1"]]))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              xaxis=dict(color="white"), yaxis=dict(color="white"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada cukup data komentar untuk analisis kata.")
    with col_b:
        if corpus.strip():
            wc = WordCloud(width=600, height=400, background_color=None, mode="RGBA", colormap="plasma").generate(corpus)
            fig_wc, ax_wc = plt.subplots(figsize=(6, 4))
            fig_wc.patch.set_alpha(0.0)
            ax_wc.imshow(wc, interpolation="bilinear")
            ax_wc.axis("off")
            st.pyplot(fig_wc)
        else:
            st.info("Belum ada komentar untuk membuat WordCloud.")

    st.markdown("---")

    # ============================================================
    # 🔙 Navigasi
    # ============================================================
    st.button(
        "⬅️ Kembali ke Self Reflection",
        on_click=lambda: st.session_state.update({'tab_selection': 'Self Reflection'})
    )
