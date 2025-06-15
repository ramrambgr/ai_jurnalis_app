def generate_prompt(caption_text, user_input, language="id", reference_text=None, metadata=None, style_guidance=None):
    """
    Buat prompt untuk menulis artikel berita.

    Args:
        caption_text (str): Deskripsi gambar.
        user_input (str): Permintaan atau fokus artikel dari pengguna.
        language (str): Kode bahasa ('id' atau 'en').
        reference_text (str, optional): Teks referensi faktual.
        metadata (dict, optional): Metadata gambar.
        style_guidance (str, optional): Panduan gaya penulisan (misal judul viral).
    Returns:
        str: Prompt lengkap untuk model.
    """
    if language == "en":
        prompt = f"Image description: {caption_text}\n"
        if metadata:
            prompt += f"Image metadata (excluding GPS coordinates): {metadata}\n"
        prompt += f"User request: {user_input}\n"
        if reference_text:
            prompt += f"\nAdditional references:\n{reference_text}\n"
        if style_guidance:
            prompt += f"\nStyle guidance (example headlines):\n{style_guidance}\n"
        prompt += "\nPlease write a complete, detailed, and factual news article."
    else:
        prompt = f"Deskripsi gambar: {caption_text}\n"
        if metadata:
            prompt += f"Metadata gambar (tanpa koordinat GPS): {metadata}\n"
        prompt += f"Permintaan pengguna: {user_input}\n"
        if reference_text:
            prompt += f"\nReferensi tambahan:\n{reference_text}\n"
        if style_guidance:
            prompt += f"\nPanduan gaya penulisan (contoh judul):\n{style_guidance}\n"
        prompt += "\nSilakan tulis artikel berita yang lengkap, mendalam, dan faktual."
    return prompt


def generate_response(model, prompt):
    """
    Panggil model untuk menghasilkan respons teks berdasarkan prompt.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gagal menghasilkan respons dari model: {e}"