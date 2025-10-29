import pandas as pd
import re
import pickle
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import streamlit as st

# =====================================================
# 1️⃣ LOAD RESOURCE (kamus alay, stopword, stemmer)
# =====================================================
@st.cache_resource
def load_resources():
    """Load kamus alay, stopword list, dan stemmer hanya sekali."""
    alay_dict = pd.read_csv('data/new_kamusalay.csv', encoding='latin-1', header=None)
    alay_dict_map = dict(zip(alay_dict[0], alay_dict[1]))

    stopword = pd.read_csv('data/stopwordbahasa.csv', header=None)
    stopword_list = stopword[0].tolist()

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return alay_dict_map, stopword_list, stemmer


# =====================================================
# 2️⃣ TEXT PREPROCESSING
# =====================================================
def preprocess(text, alay_dict_map, stopword_list, stemmer):
    """Lakukan pembersihan teks sebelum diklasifikasi."""
    text = text.lower()
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)                # hilangkan simbol
    text = re.sub('rt|user|www|https?://\S+', ' ', text)     # hilangkan tag user/url
    text = ' '.join([alay_dict_map.get(w, w) for w in text.split()])  # ubah alay
    text = stemmer.stem(text)
    text = ' '.join([w for w in text.split() if w not in stopword_list])
    return re.sub(r'\s+', ' ', text).strip()


# =====================================================
# 3️⃣ LOAD MODEL & VECTORIZER
# =====================================================
@st.cache_resource
def load_models():
    """Load semua model & vectorizer dari file pickle."""
    with open('models/models.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['models'], data['vectorizers']


# =====================================================
# 4️⃣ PREDIKSI LABEL
# =====================================================
def predict_labels(text, models, vectorizers, alay_dict_map, stopword_list, stemmer):
    """Prediksi multi-label hate speech dengan ambang batas tertentu."""
    clean = preprocess(text, alay_dict_map, stopword_list, stemmer)
    results = {}

    for label, model in models.items():
        vec = vectorizers[label].transform([clean])
        proba = model.predict_proba(vec)[0, 1]

        # Logika label
        if proba > 0.58:
            status = "🔴 Hate Speech"
        elif 0.42 <= proba <= 0.58:
            status = "🟡 Potensi Bias"
        else:
            status = "🟢 Etis / Aman"

        results[label] = {
            "Probability": round(proba, 2),
            "Status": status
        }

    return results


# =====================================================
# 5️⃣ CUSTOM ALERT BOXES (pengganti st.info/dll)
# =====================================================

def info_box(text):
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #2A5C7D, #4A8BB0);
        color: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: 500;
        text-align: justify;
        text-justify: inter-word;
        word-wrap: break-word;
        hyphens: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        line-height: 1.6;
    ">
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def success_box(text):
    st.markdown(f"""
    <div style="
        background-color: #2E8B57;
        color: #F8FAFC;
        padding: 1rem;
        border-left: 4px solid #38C172;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-weight: 500;
        text-align: justify;
        text-justify: inter-word;
        word-wrap: break-word;
        hyphens: auto;
    ">
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def warning_box(text):
    st.markdown(f"""
    <div style="
        background-color: #D97706;
        color: #F8FAFC;
        padding: 1rem;
        border-left: 4px solid #F59E0B;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-weight: 500;
        text-align: justify;
        text-justify: inter-word;
        word-wrap: break-word;
        hyphens: auto;
    ">
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def error_box(text):
    st.markdown(f"""
    <div style="
        background-color: #B91C1C;
        color: #F8FAFC;
        padding: 1rem;
        border-left: 4px solid #EF4444;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-weight: 500;
        text-align: justify;
        text-justify: inter-word;
        word-wrap: break-word;
        hyphens: auto;
    ">
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)
