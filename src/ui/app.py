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
def load_index():
    connection = sqlite3.connect("data/memory.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, filename, embedding FROM screenshots")
    rows = cursor.fetchall()
    connection.close()

    filenames = []
    embeddings = []

    for row_id, filename, embedding_text in rows:
        numbers = [float(x) for x in embedding_text.split(",")]
        filenames.append(filename)
        embeddings.append(numbers)

    embeddings_array = np.array(embeddings).astype("float32")
    index = faiss.IndexFlatL2(512)
    index.add(embeddings_array)

    return index, filenames

model, preprocess, device = load_model()
index, filenames = load_index()

query_text = st.text_input("Search your screen history:")

if query_text:
    text_input = clip.tokenize([query_text]).to(device)
    with torch.no_grad():
        query_embedding = model.encode_text(text_input)

    query_array = query_embedding.cpu().numpy().astype("float32")

    k = 3
    distances, indices = index.search(query_array, k)

    st.subheader(f"Top {k} matches:")

    for rank, idx in enumerate(indices[0]):
        filename = filenames[idx]
        image_path = os.path.join("data/screenshots", filename)
        st.image(image_path, caption=f"{rank+1}. {filename} (distance: {distances[0][rank]:.4f})")