import streamlit as st

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="ETHICATOR - Ethical Communication AI Moderator",
    layout="wide",
    page_icon="💬"
)

from modules.sidebar import show_sidebar
from tabs import (
    tab1_welcome_hub, tab2_ethics_lab, tab3_ethics_academy,
    tab4_self_reflection, tab5_ethics_dashboard, tab5_ethics_dashboard,
)

# -------------------------
# Styling umum (CSS)
# -------------------------
st.markdown("""
<style>
/* =============================
   🎨 Sidebar & Konten
   ============================= */
[data-testid="stSidebar"] {
    background-color: #142B45 !important;  
    color: #F8FAFC !important;             
    padding: 10px !important;
}
[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* =============================
   🌊 Konten utama gradasi biru
   ============================= */
.stApp {
    background: linear-gradient(to right, #1B3B5C, #2A5C7D, #4A8BB0) !important;
    color: #F8FAFC !important;             
    min-height: 100vh !important;
}

/* =============================
   🧱 Layout utama
   ============================= */
.block-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
@media (max-width: 1000px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 95% !important;
    }
}

/* =============================
   📝 Judul & subheader
   ============================= */
h1, h2, h3, .stText, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #F8FAFC !important;
}

/* =============================
   🔘 Tombol
   ============================= */
.stButton>button {
    background-color: #0EA5E9 !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton>button:hover {
    background-color: #0284C7 !important;
    transform: scale(1.02) !important;
}

/* =============================
   📊 Tabel
   ============================= */
.stDataFrame th {
    background-color: #142B45 !important;
    color: #F8FAFC !important;
    text-align: center !important;
}
.stDataFrame td {
    text-align: center !important;
    color: #F8FAFC !important;
}

/* =============================
   🔗 Link interaktif
   ============================= */
a, a:link, a:visited {
    color: #D0F4F4 !important;
    text-decoration: none !important;
}
a:hover {
    color: #A0E0E0 !important;
    text-decoration: underline !important;
}

/* =============================
   💬 Teks biasa
   ============================= */
.stMarkdown p, .stText {
    color: #F8FAFC !important;
}

/* =============================
   👤 Input username
   ============================= */
[data-testid="stTextInput"][key="username_input"] input {
    color: navy !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Fungsi Footer
# -------------------------
def show_footer():
    st.markdown("""
        <div style='width: 100%; font-size:13px; text-align: center; color: gray; padding: 10px; margin-top: 80px;'>
            © 2025 Difta Alzena Sakhi · UPN “Veteran” Jawa Timur
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# Sidebar + logo + login
# -------------------------
show_sidebar()

# -------------------------
# Navigasi tab default
# -------------------------
tab = st.sidebar.radio(
    "Choose Page:",
    [
        "Welcome Hub",
        "Ethics Lab",
        "Ethics Academy",
        "Self Reflection",
        "Ethics Dashboard"
    ],
    key="tab_selection"
)


# -------------------------
# Routing tab
# -------------------------
if tab == "Welcome Hub":
    tab1_welcome_hub.run()
elif tab == "Ethics Lab":
    tab2_ethics_lab.run()
elif tab == "Ethics Academy":
    tab3_ethics_academy.run()
elif tab == "Self Reflection":
    tab4_self_reflection.run()
elif tab == "Ethics Dashboard":
    tab5_ethics_dashboard.run()

# -------------------------
# Footer
# -------------------------
show_footer()
