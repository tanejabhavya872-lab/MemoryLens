import streamlit as st
import sqlite3
import numpy as np
import faiss
import torch
import clip
import os

st.title("AI Digital Memory Assistant")

@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, device

@st.cache_resource
def load_data():
    connection = sqlite3.connect("data/memory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, filename, ocr_text, embedding FROM screenshots")
    rows = cursor.fetchall()
    connection.close()

    filenames = []
    ocr_texts = []
    embeddings = []

    for row_id, filename, ocr_text, embedding_text in rows:
        numbers = [float(x) for x in embedding_text.split(",")]
        filenames.append(filename)
        ocr_texts.append(ocr_text if ocr_text else "")
        embeddings.append(numbers)

    embeddings_array = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(512)
    index.add(embeddings_array)

    return index, filenames, ocr_texts

model, preprocess, device = load_model()
index, filenames, ocr_texts = load_data()

query_text = st.text_input("Search your screen history:")

if query_text:
    text_input = clip.tokenize([query_text]).to(device)
    with torch.no_grad():
        query_embedding = model.encode_text(text_input)

    query_array = query_embedding.cpu().numpy().astype("float32")

    total_screenshots = len(filenames)
    distances, indices = index.search(query_array, total_screenshots)

    max_distance = distances[0].max()

    results = []

    for rank, idx in enumerate(indices[0]):
        distance = distances[0][rank]
        semantic_score = 1 - (distance / max_distance)

        keyword_bonus = 0
        if query_text.lower() in ocr_texts[idx].lower():
            keyword_bonus = 1.0

        final_score = semantic_score + keyword_bonus

        results.append({
            "filename": filenames[idx],
            "semantic_score": semantic_score,
            "keyword_bonus": keyword_bonus,
            "final_score": final_score
        })

    results.sort(key=lambda r: r["final_score"], reverse=True)

    st.subheader("Top matches:")

    for rank, result in enumerate(results[:5]):
        image_path = os.path.join("data/screenshots", result["filename"])
        match_type = "Keyword + Semantic match" if result["keyword_bonus"] > 0 else "Semantic match"
        st.image(
            image_path,
            caption=f"{rank+1}. {result['filename']} — {match_type} (score: {result['final_score']:.3f})"
        )