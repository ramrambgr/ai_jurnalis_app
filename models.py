import streamlit as st
import google.generativeai as genai

def load_gemini_model(api_key=None):
    """
    Fungsi untuk memuat model Gemini 1.5 Flash.
    Mengambil API key dari Streamlit secrets dan memastikan konfigurasi benar.
    Kompatibel untuk teks & gambar (multimodal).
    """

    # 🔐 Ambil API Key dari Streamlit Secrets jika tidak diberikan langsung
    api_key = api_key or st.secrets["GEMINI_API_KEY"]

    # ⚙️ Konfigurasi API
    genai.configure(api_key=api_key)

    # ✅ Gunakan model stabil tanpa '-latest'
    model_name = "gemini-1.5-flash"

    # 🧠 Buat instance model generatif
    try:
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"❌ Gagal memuat model '{model_name}': {e}")
        return None
