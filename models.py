import streamlit as st
import google.generativeai as genai

def load_gemini_model(api_key=None):
    """
    Fungsi untuk memuat model Gemini 1.5 Flash dengan konfigurasi Streamlit Secrets.
    Secara otomatis menggunakan API key dari .streamlit/secrets.toml.
    """

    # Ambil API Key dari Streamlit Secrets jika tidak diberikan langsung
    api_key = api_key or st.secrets["GEMINI_API_KEY"]

    # Konfigurasi Gemini API
    genai.configure(api_key=api_key)

    # Gunakan nama model yang benar (versi terbaru)
    model_name = "gemini-1.5-flash-latest"

    # Buat instance model
    model = genai.GenerativeModel(model_name)

    return model
