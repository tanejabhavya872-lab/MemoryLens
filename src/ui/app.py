import streamlit as st
import requests
import os

st.title("AI Digital Memory Assistant")

query_text = st.text_input("Search your screen history:")

if query_text:
    response = requests.get("http://127.0.0.1:8000/search", params={"query": query_text})
    data = response.json()
    results = data["results"]

    st.subheader("Top matches:")
    for rank, result in enumerate(results):
        image_path = os.path.join("data/screenshots", result["filename"])
        match_type = "Keyword + Semantic match" if result["keyword_bonus"] > 0 else "Semantic match"
        st.image(
            image_path,
            caption=f"{rank+1}. {result['filename']} — {match_type} (score: {result['final_score']:.3f})"
        )