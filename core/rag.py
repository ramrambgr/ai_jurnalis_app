# File: core/rag.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

def split_into_chunks(text: str, chunk_size: int = 300) -> list[str]:
    words = clean_text(text).split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def retrieve_relevant_chunks(
    user_query: str,
    reference_text: str,
    top_k: int = 3
) -> list[str]:
    if not reference_text:
        return []
    chunks = split_into_chunks(reference_text)
    docs = [user_query] + chunks
    tfidf = TfidfVectorizer().fit_transform(docs)
    cos_sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    top_indices = cos_sim.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

def compute_similarity_score(text_a: str, text_b: str) -> float:
    """
    Hitung skor kemiripan semantik antara dua teks menggunakan TF-IDF dan cosine similarity.
    """
    if not text_a or not text_b:
        return 0.0
    texts = [text_a, text_b]
    vectorizer = TfidfVectorizer().fit_transform(texts)
    sim_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    return float(sim_matrix[0][0])  # hasil antara 0 (tidak mirip) sampai 1 (identik)
