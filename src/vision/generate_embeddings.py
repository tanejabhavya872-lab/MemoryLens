import torch
import clip
from PIL import Image
import sqlite3
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

connection = sqlite3.connect("data/memory.db")
cursor = connection.cursor()

cursor.execute("SELECT id, filename FROM screenshots")
rows = cursor.fetchall()

for row_id, filename in rows:
    image_path = os.path.join("data/screenshots", filename)
    image = Image.open(image_path)
    image_input = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image_input)

    embedding_list = embedding[0].tolist()
    embedding_text = ",".join([str(x) for x in embedding_list])

    cursor.execute("""
        UPDATE screenshots
        SET embedding = ?
        WHERE id = ?
    """, (embedding_text, row_id))

    print(f"Processed: {filename}")

connection.commit()
connection.close()

print("All embeddings generated and saved.")