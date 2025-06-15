import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def load_gemini_model(api_key=None):
    api_key = api_key or os.getenv("AIzaSyCqcMN3u6xQNAvPc-kdff5N_GKFsCadOMo")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")