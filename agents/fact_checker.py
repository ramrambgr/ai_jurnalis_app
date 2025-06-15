# agents/fact_checker.py

def fact_check_article(model, article_text, reference_text=None, language="id"):
    try:
        if language == "en":
            prompt = f"""
Check the following article for factual accuracy. 
Compare it with any available reference material and flag inconsistencies or vague claims.

Article:
{article_text}

References:
{reference_text or 'No references provided.'}

Return a summary of findings and suggested corrections.
"""
        else:
            prompt = f"""
Periksa keakuratan fakta dalam artikel berikut. 
Bandingkan dengan referensi yang tersedia dan tandai bagian yang tidak konsisten atau klaim yang tidak jelas.

Artikel:
{article_text}

Referensi:
{reference_text or 'Tidak ada referensi yang diberikan.'}

Kembalikan ringkasan temuan dan saran perbaikan.
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gagal memeriksa fakta: {e}"
