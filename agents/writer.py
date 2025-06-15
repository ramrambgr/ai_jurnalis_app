from prompts import generate_prompt, generate_response
from core.rag import retrieve_relevant_chunks

def write_article(
    model,
    caption_text,
    user_input,
    language_code,
    reference_text=None,
    metadata=None,
    style_guidance=None,
    mode="komprehensif",
    use_rag: bool = False
):
    """
    Tulis artikel berdasarkan gambar dan permintaan pengguna.

    Args:
        model: instance model generatif.
        caption_text: deskripsi gambar.
        user_input: masukan pengguna (topik/fokus).
        language_code: 'id' atau 'en'.
        reference_text: teks referensi faktual.
        metadata: metadata gambar.
        style_guidance: contoh gaya penulisan (judul viral).
        mode: gaya penulisan ('komprehensif', 'ringkas', 'naratif').
        use_rag: flag untuk mengaktifkan RAG.
    Returns:
        Teks artikel yang dihasilkan.
    """
    # Gunakan potongan referensi jika RAG diaktifkan dan teks tersedia
    if use_rag and reference_text:
        chunks = retrieve_relevant_chunks(user_input, reference_text)
        reference_for_prompt = "\n\n".join(chunks)
    else:
        reference_for_prompt = reference_text

    # Bangun prompt
    prompt = generate_prompt(
        caption_text,
        user_input,
        language=language_code,
        reference_text=reference_for_prompt,
        metadata=metadata,
        style_guidance=style_guidance
    )

    # Tambah instruksi gaya penulisan
    if mode == "komprehensif":
        prompt += "\nTulis artikel dalam 3 bagian: pembuka, isi utama, dan penutup."
    elif mode == "ringkas":
        prompt += "\nTulis artikel dalam bentuk ringkasan padat tapi faktual."
    elif mode == "naratif":
        prompt += "\nGunakan gaya penceritaan yang naratif dan menarik."

    # Generate artikel dari model
    return generate_response(model, prompt)
