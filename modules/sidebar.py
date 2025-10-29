import streamlit as st
import os

def show_sidebar():
    # --- Logo Section ---
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.jpg")

    # --- Sidebar CSS Styling ---
    st.sidebar.markdown("""
        <style>
        /* Sidebar warna & padding */
        [data-testid="stSidebar"] {
            background-color: #142B45;
            color: #F8FAFC;
            padding: 10px;
        }

        /* Hapus margin atas logo */
        .logo-img img {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }

        .sidebar-content {
            margin-bottom: 20px;
        }

        .sidebar-footer {
            font-size: 12px;
            color: #AFCBFF;
            text-align: center;
            padding: 10px 0;
        }

        .sidebar-divider {
            border-top: 1px solid #2A5C7D;
            margin: 10px 0;
        }

        /* Label font besar sama dengan login */
        .sidebar-label {
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 5px;
        }

        /* Warna teks input username navy (Streamlit terbaru) */
        [data-baseweb="input"] input {
            color: #1B3B5C !important;
            font-weight: 600 !important;
        }

        /* Styling gradasi greeting */
        .greeting-box {
            background: linear-gradient(to right, #1B3B5C, #2A5C7D);
            color: #F8FAFC;
            padding: 12px;
            border-radius: 8px;
            font-weight: 600;
            margin-bottom: 10px;
            text-align: center;
        }

        /* Styling tombol Login / Logout */
        .stButton>button {
            background: linear-gradient(to right, #1B3B5C, #2A5C7D);
            color: #F8FAFC;
            font-weight: 600;
            border-radius: 8px;
            padding: 6px 12px;
            border: none;
            width: 100%;
            cursor: pointer;
            margin-top: 5px;
        }

        /* Hover effect */
        .stButton>button:hover {
            background: linear-gradient(to right, #2A5C7D, #1B3B5C);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Sidebar Main Content ---
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    # Logo
    if os.path.exists(logo_path):
        st.sidebar.markdown('<div class="logo-img">', unsafe_allow_html=True)
        st.sidebar.image(logo_path, use_container_width=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    else:
        st.sidebar.warning("Logo tidak ditemukan di folder assets/")

    # --- Login / Selamat Datang ---
    st.sidebar.markdown('<div class="sidebar-label">🔐 Login ke ETHICATOR</div>', unsafe_allow_html=True)

    # Input username hanya jika belum login
    if "username" not in st.session_state:
        username = st.sidebar.text_input("Masukkan nama panggilan kamu:", key="username_input")
        if st.sidebar.button("Login"):
            if username:
                st.session_state.username = username
                # Greeting dengan background gradasi
                st.sidebar.markdown(
                    f'<div class="greeting-box">🌿 Selamat datang, {username}!<br>Let\'s build ethical digital habits today!</div>',
                    unsafe_allow_html=True
                )
            else:
                st.sidebar.warning("Masukkan nama dulu ya~")
    else:
        # Jika sudah login, tampilkan greeting dengan gradasi + tombol logout
        st.sidebar.markdown(
            f'<div class="greeting-box">🌿 Selamat datang, {st.session_state.username}!<br>Let\'s build ethical digital habits today!</div>',
            unsafe_allow_html=True
        )
        if st.sidebar.button("Logout"):
            del st.session_state.username

    # Divider sebelum pilih tab
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # Tutup div utama
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
