import streamlit as st
import google.generativeai as genai

def load_gemini_model(api_key=None):
    api_key = api_key or st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")
