import sqlite3
import numpy as np
import faiss
import torch
import clip

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

cursor.execute("SELECT id, filename, embedding FROM screenshots")
rows = cursor.fetchall()

ids = []
filenames = []
embeddings = []

for row_id, filename, embedding_text in rows:
    numbers = [float(x) for x in embedding_text.split(",")]
    ids.append(row_id)
    filenames.append(filename)
    embeddings.append(numbers)

embeddings_array = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(512)
index.add(embeddings_array)

query_text = "a screenshot of a code editor"
text_input = clip.tokenize([query_text]).to(device)
with torch.no_grad():
    query_embedding = model.encode_text(text_input)

query_array = query_embedding.cpu().numpy().astype("float32")

k = 3
distances, indices = index.search(query_array, k)

print(f"Top {k} matches for: '{query_text}'")
for rank, idx in enumerate(indices[0]):
    print(f"{rank+1}. {filenames[idx]} (distance: {distances[0][rank]:.4f})")