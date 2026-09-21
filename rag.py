import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "waste_guidance.json"


def load_knowledge():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_documents(records):
    documents = []

    for record in records:
        text = (
            f"Category: {record['category']}\n"
            f"Keywords: {record['keywords']}\n"
            f"Preparation: {record['preparation']}\n"
            f"Route: {record['route']}\n"
            f"Caution: {record['caution']}\n"
            f"Source: {record['source']}"
        )
        documents.append(text)

    return documents


def retrieve_guidance(query: str, top_k: int = 3):
    records = load_knowledge()
    documents = build_documents(records)

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, document_vectors)[0]

    ranked_indices = similarities.argsort()[::-1]
    results = []

    for index in ranked_indices[:top_k]:
        results.append({
            "text": documents[index],
            "score": float(similarities[index]),
        })

    return results
