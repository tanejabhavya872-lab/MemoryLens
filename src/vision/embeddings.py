import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_embedding(image_path):
    image = Image.open(image_path)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image_input)
    return embedding

def get_text_embedding(text):
    text_input = clip.tokenize([text]).to(device)
    with torch.no_grad():
        embedding = model.encode_text(text_input)
    return embedding

image_embedding = get_image_embedding("data/screenshots/2026-07-13_18-12-17.png")
text_embedding = get_text_embedding("a photo of a beach with palm trees")

similarity = torch.nn.functional.cosine_similarity(image_embedding, text_embedding)
print(f"Similarity: {similarity.item()}")