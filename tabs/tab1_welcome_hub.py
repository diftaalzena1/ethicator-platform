# tabs/tab1_welcome_hub.py
import streamlit as st
from utils import info_box

def run():
    """
    Halaman Home ETHICATOR.
    Menampilkan:
    - Header selamat datang
    - Module card: Tentang ETHICATOR
    - Hero section: Tantangan & Solusi (2 kolom)
    - Fitur utama (grid card, tanpa About)
    - CTA ke Ethics Lab
    """

    username = st.session_state.get('username', 'Pengguna')  # default jika username belum ada

    # ==============================
    # Fungsi module card klikable
    # ==============================
    def module_card(title, desc, tab_target, bg_color="#0EA5E9", text_color="#F8FAFC"):
        html = f"""
        <div style="
            background: linear-gradient(135deg, {bg_color} 0%, rgba(255,255,255,0.05) 100%);
            color: {text_color};
            padding: 1.4rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        " onClick="window.location.href='#{tab_target}'" 
             onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.3)'" 
             onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 10px rgba(0,0,0,0.2)'">
            <h4>{title}</h4>
            <p style='font-size:14px; margin-top:5px;'>{desc}</p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    # ==============================
    # Header (Centered, Personal)
    # ==============================
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:20px;">
        <h1 style="color:#F8FAFC; font-size:36px; margin-bottom:10px;">
            👋 Selamat Datang, {username}! 
        </h1>
        <h3 style="color:#e0e0e0; font-weight:600;">di ETHICATOR — Your Ethical Communication AI Moderator</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ==============================
    # Module Card: Tentang ETHICATOR
    # ==============================
    module_card(
        title="ℹ️ Tentang ETHICATOR",
        desc=("ETHICATOR adalah asisten AI interaktif yang dirancang untuk mendampingi dan memoderasi etika komunikasi digital "
              "di kalangan generasi muda. Proyek ini menggabungkan teknologi AI dengan nilai-nilai empati dan tanggung jawab sosial."),
        tab_target="About ETHICATOR",
        bg_color="rgba(107,114,128,0.3)"
    )

    st.markdown("---")

    # ==============================
    # Hero Section — Tantangan & Solusi
    # ==============================
    st.markdown("### 🌐 Tantangan & Solusi Dunia Digital")
    st.markdown(
        "<div style='font-size:14px; color:#d0d0d0;'>Pelajari tantangan komunikasi digital dan bagaimana ETHICATOR membantu mengatasinya.</div>",
        unsafe_allow_html=True
    )
    st.markdown("")

    cols_hero = st.columns(2)

    with cols_hero[0]:
        module_card(
            title="⚠️ Tantangan Dunia Digital",
            desc=("Di era media sosial, ujaran kebencian, disinformasi, dan perundungan daring "
                  "semakin sering muncul dan memengaruhi iklim komunikasi publik."),
            tab_target="Tantangan",
            bg_color="rgba(239,68,68,0.3)",
            text_color="#F8FAFC"
        )

    with cols_hero[1]:
        module_card(
            title="🧠 ETHICATOR Hadir Sebagai Solusi",
            desc=("Dengan pendekatan Ethical AI Companion, ETHICATOR mendeteksi ujaran kebencian secara real-time, "
                  "memberikan refleksi etis sebelum komentar dikirim, membangun kesadaran moral digital, "
                  "dan meningkatkan empati serta tanggung jawab pengguna."),
            tab_target="Solusi",
            bg_color="rgba(14,165,233,0.3)",
            text_color="#F8FAFC"
        )

    st.markdown("---")

    # ==============================
    # Fitur-Fitur Utama ETHICATOR (Grid Cards)
    # ==============================
    st.markdown("### ✨ Fitur Utama ETHICATOR")
    st.markdown("<div style='font-size:14px; color:#d0d0d0;'>Pilih modul untuk mulai belajar dan eksplorasi etika komunikasi digital.</div>", unsafe_allow_html=True)
    st.markdown("")

    screen_width = st.query_params.get("screen_width", [1200])[0]
    try:
        screen_width = int(screen_width)
    except:
        screen_width = 1200

    if screen_width > 1000:
        cols = st.columns(3)
    elif screen_width > 600:
        cols = st.columns(2)
    else:
        cols = st.columns(1)

    with cols[0]:
        module_card(
            "🧪 Ethics Lab",
            "Uji komentar & lihat bagaimana AI menilai tingkat etisnya",
            "Ethics Lab",
            bg_color="rgba(14,165,233,0.3)"
        )
    with cols[1]:
        module_card(
            "🎓 Ethics Academy",
            "Belajar prinsip komunikasi etis & literasi digital interaktif",
            "Ethics Academy",
            bg_color="rgba(234,179,8,0.3)"
        )
    if len(cols) > 2:
        with cols[2]:
            module_card(
                "🪞 Self Reflection",
                "Catat refleksi pribadi harian untuk mengukur empati digital",
                "Self Reflection",
                bg_color="rgba(16,185,129,0.3)"
            )

    # Baris kedua hanya berisi satu kolom (tanpa About)
    st.markdown("")
    module_card(
        "🖥️ Ethics Dashboard",
        "Pantau progres kesadaran etis, statistik personal, & rekomendasi pengembangan diri",
        "Ethics Dashboard",
        bg_color="rgba(236,72,153,0.3)"
    )

    st.markdown("---")

    # ==============================
    # CTA (Call to Action)
    # ==============================
    info_box("""
    <div style='text-align:center;'>
        💡 <b>Mulai Eksplorasi:</b> Coba tab <b>🧪 Ethics Lab</b> untuk komunikasi digital yang lebih sopan, bijak, dan empatik.
    </div>
    """)

    st.markdown("---")

    # ==============================
    # Navigasi ke Ethics Lab
    # ==============================
    st.button("➡️ Masuk ke Ethics Lab", 
            on_click=lambda: st.session_state.update({'tab_selection': 'Ethics Lab'}))
