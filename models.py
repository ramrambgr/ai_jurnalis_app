import streamlit as st
import google.generativeai as genai

def load_gemini_model(api_key=None):
    api_key = api_key or st.secrets["AIzaSyCqcMN3u6xQNAvPc-kdff5N_GKFsCadOMo"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")
