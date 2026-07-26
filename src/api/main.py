from fastapi import FastAPI
import sqlite3
import numpy as np
import faiss
import torch
import clip

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

connection = sqlite3.connect("data/memory.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("SELECT id, filename, ocr_text, embedding FROM screenshots")
rows = cursor.fetchall()

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


@app.get("/search")
def search(query: str):
    text_input = clip.tokenize([query]).to(device)
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
        if query.lower() in ocr_texts[idx].lower():
            keyword_bonus = 1.0
        final_score = semantic_score + keyword_bonus
        results.append({
            "filename": filenames[idx],
            "semantic_score": float(semantic_score),
            "keyword_bonus": float(keyword_bonus),
            "final_score": float(final_score)
        })

    results.sort(key=lambda r: r["final_score"], reverse=True)
    return {"results": results[:5]}