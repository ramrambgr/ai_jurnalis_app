# agents/image_interpreter.py

def describe_image(model, image, mode="caption", language="id"):
    try:
        if language == "en":
            prompts = {
                "caption": "Describe this image in a detailed, narrative, journalistic style. Focus on what can be inferred and observed.",
                "emotion": "Analyze the emotions or atmosphere in this image, as if reporting it in the news.",
                "context": "What is likely happening in this image? Provide journalistic insight."
            }
        else:
            prompts = {
                "caption": "Deskripsikan gambar ini secara naratif dan detail dalam gaya jurnalisme. Fokus pada apa yang terlihat dan dapat disimpulkan.",
                "emotion": "Analisa suasana atau ekspresi dalam gambar ini seolah sedang dilaporkan di berita.",
                "context": "Menurutmu, apa yang kemungkinan besar terjadi dalam gambar ini? Berikan wawasan jurnalis."
            }

        prompt = prompts.get(mode, prompts["caption"])
        response = model.generate_content([image, prompt])
        return response.text.strip()
    except Exception as e:
        return f"❌ Gagal membuat deskripsi gambar: {e}"
