import re

def agent_planner(caption: str, user_input: str) -> dict:
    steps, questions, goals = [], [], []

    if "video" in user_input.lower():
        goals.append("Tulis skrip narasi untuk video")
    elif "investigasi" in user_input.lower():
        goals.append("Tulis artikel investigatif dengan alur kronologis")
        questions.append("Apakah Anda memiliki data waktu atau lokasi kejadian?")
    else:
        goals.append("Tulis artikel berita yang lengkap, mendalam, dan faktual")

    if re.search(r"(identitas|siapa|tokoh)", user_input.lower()):
        steps.append("Analisa gambar untuk mendeteksi tokoh atau objek penting")

    if "reaksi" in user_input.lower() or "opini" in user_input.lower():
        steps.append("Sertakan pendapat publik atau sumber relevan")

    if not caption or caption.strip() == "":
        steps.append("Buat deskripsi gambar lebih dulu")

    if re.search(r"(data|statistik|tren)", user_input.lower()):
        steps.append("Cek data pendukung atau tren terkini")

    return {
        "goals": goals,
        "steps": steps,
        "questions": questions,
        "topic_keywords": extract_keywords(user_input)
    }

def extract_keywords(text):
    keywords = re.findall(r"\b\w{5,}\b", text.lower())
    stopwords = {"dengan", "untuk", "tentang", "berita", "artikel", "menulis"}
    return list(set(k for k in keywords if k not in stopwords))
