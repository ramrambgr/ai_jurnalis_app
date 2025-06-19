# ===================== [IMPORT LIBRARY] =====================
import streamlit as st
from PIL import Image
import json
import os

from models import load_gemini_model
from agents.image_interpreter import describe_image
from agents.planner import agent_planner
from agents.writer import write_article
from agents.fact_checker import fact_check_article
from agents.headline_generator import generate_headlines
from core.utils import extract_exif_data, read_reference_file
from scraper import get_all_viral_news
from core.rag import retrieve_relevant_chunks

# ===================== [UI KONFIGURASI DASAR] =====================
st.set_page_config(page_title="AI Assistant Jurnalis", layout="wide")
st.title("📰 AI Assistant Jurnalis")

# ===================== [INPUT GAMBAR & PILIHAN BAHASA] =====================
uploaded_file = st.file_uploader("📷 Upload Gambar", type=["jpg", "jpeg", "png"])
language = st.selectbox("🌐 Bahasa Output", ["Bahasa Indonesia", "English"])
lang_code = "id" if language == "Bahasa Indonesia" else "en"

# ===================== [MODE ARTIKEL & INPUT USER] =====================
mode_option = st.radio("🧠 Mode Artikel:", ["Generate Langsung", "Gunakan Keterangan Tambahan"])
user_input = (
    st.text_area("🗣️ Tulis keterangan/fokus artikel:", height=100)
    if mode_option == "Gunakan Keterangan Tambahan" else
    "Tulis artikel berita yang lengkap, mendalam, dan faktual."
)

# ===================== [PILIHAN GAYA PENULISAN] =====================
penulisan_mode = st.radio("✍️ Gaya Penulisan:", ["Komprehensif", "Ringkas", "Naratif"])
mode_map = {"Komprehensif": "komprehensif", "Ringkas": "ringkas", "Naratif": "naratif"}
mode = mode_map[penulisan_mode]

# ===================== [RAG SETTINGS] =====================
st.header("⚙️ RAG Settings")
use_rag = st.checkbox("Aktifkan RAG (ambil potongan referensi)")
ref_text, raw_articles = None, []
if use_rag:
    rag_source = st.selectbox("Pilih Sumber Referensi:", ["File Upload (.txt/.pdf/.docx)", "Berita Viral Scraping"])
    if rag_source == "File Upload (.txt/.pdf/.docx)":
        ref_file = st.file_uploader("📄 Upload Referensi (.txt/.pdf/.docx)", type=["txt", "pdf", "docx"])
        if ref_file:
            ref_text = read_reference_file(ref_file)
    else:
        if not os.path.exists("berita_viral.json"):
            raw_articles = get_all_viral_news()
        else:
            with open("berita_viral.json", "r", encoding="utf-8") as f:
                raw_articles = json.load(f)
        st.markdown("#### Daftar Berita Viral dari Scraping:")
        for art in raw_articles:
            st.markdown(f"- **{art['sumber']}**: [{art['judul']}]({art['url']})")
            st.caption(art['ringkasan'])
        ref_text = "\n".join(a['ringkasan'] for a in raw_articles)

# ===================== [STYLE HEADLINE PANDUAN] =====================
use_style = st.checkbox("🔎 Gunakan berita viral untuk style saja")
style_guidance = ref_text if (use_style and raw_articles) else None
if use_style and raw_articles:
    st.markdown("#### Panduan Gaya Judul Viral:")
    st.text_area("Panduan Gaya Judul Viral", value=style_guidance, height=200)

# ===================== [PENGATURAN JUDUL] =====================
st.header("⚙️ Headline Settings")
min_length = st.slider("Minimum Kata Judul", 1, 10, 3)
max_length = st.slider("Maksimum Kata Judul", min_value=min_length, max_value=20, value=12)
temp_label = st.selectbox("🎨 Tingkat Kreativitas Judul", [
    "Rendah (0.2)",
    "Sedang (0.5)",
    "Tinggi (0.7)",
    "Ekspresif (1.0)"
])
temp_map = {
    "Rendah (0.2)": 0.2,
    "Sedang (0.5)": 0.5,
    "Tinggi (0.7)": 0.7,
    "Ekspresif (1.0)": 1.0
}
temperature = temp_map[temp_label]

# ===================== [TOMBOL GENERATE & LOAD MODEL] =====================
generate_clicked = st.button("🚀 Generate Artikel")
gemini_model = load_gemini_model()

# ===================== [PROSES UTAMA SETELAH TOMBOL DIKLIK] =====================
if generate_clicked and uploaded_file:

    # === Gambar ===
    image = Image.open(uploaded_file).convert("RGB")  # ← inilah yang sebelumnya hilang
    max_width = 800
    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height), Image.LANCZOS)
    st.image(image, caption="Gambar yang diunggah", use_column_width=False)

    # === Metadata Gambar ===
    raw_meta = extract_exif_data(image)
    filtered_meta = {
        k: v for k, v in (raw_meta or {}).items()
        if not any(coord in str(k).lower() for coord in ["koordinat", "latitude", "longitude", "gps", "google"])
    }
    st.markdown("## 🧾 Metadata Gambar")
    if filtered_meta:
        st.json(filtered_meta)
    else:
        st.warning("⚠️ Tidak ada metadata EXIF ditemukan di gambar ini.")

    # === Agent 1: Image Interpreter ===
    st.markdown("## 🤖 Agent 1: Memahami Gambar")
    caption_text = describe_image(
        model=gemini_model,
        image=image,
        mode="caption",
        language=lang_code
    )
    st.text_area("📋 Deskripsi Gambar:", value=caption_text, height=100)

    # === Agent 2: Planner ===
    st.markdown("## 🧠 Agent 2: Perencana & Pertanyaan")
    plan = agent_planner(caption_text, user_input)
    for g in plan.get("goals", []): st.markdown(f"🎯 Tujuan: {g}")
    for s in plan.get("steps", []): st.markdown(f"🧭 Langkah: {s}")
    for q in plan.get("questions", []): st.info(f"❓ {q}")

    # === Agent 3: Reference Chunks (RAG) ===
    if use_rag and ref_text:
        st.markdown("## 📚 Potongan Referensi (RAG)")
        for i, chunk in enumerate(retrieve_relevant_chunks(user_input, ref_text), start=1):
            st.markdown(f"**Potongan {i}:** {chunk}")

    # === Agent 4: Writer ===
    st.markdown("## ✍️ Agent 3: Penulis Artikel")
    with st.spinner("Menulis artikel..."):
        final_article = write_article(
            gemini_model,
            caption_text,
            user_input,
            lang_code,
            reference_text=ref_text,
            metadata=filtered_meta,
            style_guidance=style_guidance,
            mode=mode,
            use_rag=use_rag
        )
        st.success("✅ Artikel selesai dibuat!")
        st.markdown("### Hasil Artikel:")
        st.markdown(final_article)
        st.download_button("📥 Download Artikel", final_article, "artikel.txt")

    # === Agent 5: Fact Checker ===
    st.markdown("## ✅ Agent 4: Pemeriksa Fakta")
    with st.spinner("Memeriksa fakta..."):
        fact_result = fact_check_article(gemini_model, final_article, ref_text, lang_code)
    st.text_area("📌 Temuan & Koreksi:", value=fact_result, height=200)

    # === Agent 6: Headline Generator ===
    st.markdown("## 📰 Agent 5: Pembuat Judul")
    with st.spinner("Menghasilkan judul..."):
        titles = generate_headlines(
            model=gemini_model,
            article_text=final_article,
            language=lang_code,
            min_words=min_length,
            max_words=max_length,
            style_guidance=style_guidance,
            jumlah=5
        )
    st.success("✅ Judul dihasilkan!")
    for idx, title in enumerate(titles, start=1):
        st.text_input(f"📝 Judul {idx}:", value=title, key=f"judul_{idx}")

    # ========== Gambar ===========
    if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    max_width = 800
    if image.width > max_width:
        ratio = max_width / float(image.width)
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height), Image.ANTIALIAS)

