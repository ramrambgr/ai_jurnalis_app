import re

def clean_headline(text: str) -> str:
    text = text.strip()
    text = re.sub(r"[.!?]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text[0].upper() + text[1:] if text else ""

def truncate_headline(headline: str, max_words: int) -> str:
    words = headline.split()
    return " ".join(words[:max_words]) if len(words) > max_words else headline

def generate_headlines(model, article_text, language="id", min_words=3, max_words=12, style_guidance=None, jumlah=5):
    try:
        if language == "en":
            prompt = (
                f"Read the article below and write {jumlah} different, compelling, concise, and relevant news headlines.\n"
                f"Each headline must be {min_words}-{max_words} words.\n"
                f"Separate each headline with a new line.\n\n"
                f"Article:\n{article_text.strip()}"
            )
            if style_guidance:
                prompt += f"\n\nExample headline styles:\n{style_guidance.strip()}"
        else:
            prompt = (
                f"Baca artikel berikut dan buat {jumlah} judul berita yang berbeda, menarik, padat, dan sesuai isi.\n"
                f"Masing-masing judul terdiri dari {min_words}-{max_words} kata.\n"
                f"Pisahkan setiap judul dengan baris baru.\n\n"
                f"{article_text.strip()}"
            )
            if style_guidance:
                prompt += f"\n\nContoh gaya judul:\n{style_guidance.strip()}"

        response = model.generate_content(contents=prompt)
        raw_text = getattr(response, 'text', str(response)).strip()
        lines = [clean_headline(line) for line in raw_text.splitlines() if line.strip()]
        cleaned = [truncate_headline(line, max_words) for line in lines if len(line.split()) >= min_words]
        return cleaned[:jumlah] if cleaned else ["❌ Tidak ada judul valid dihasilkan."]
    except Exception as e:
        return [f"❌ Gagal membuat judul: {e}"]
