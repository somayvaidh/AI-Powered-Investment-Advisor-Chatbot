import json
import os
from tqdm import tqdm
import sys
from sentence_transformers import SentenceTransformer

# Add parent path to import other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load model (you can switch to others like 'all-mpnet-base-v2')
MODEL_NAME = "all-MiniLM-L6-v2"

class Embedder:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, show_progress_bar=False).tolist()

def load_news_data(filepath="semantic_cache/news_cache.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_news_articles(articles, embedder):
    embedded_data = []
    for article in tqdm(articles, desc="Embedding news"):
        summary = article.get("detailed_summary", "")
        if not summary:
            continue

        embedding = embedder.embed_text(summary)
        if embedding:
            embedded_data.append({
                "symbol": article["symbol"],
                "title": article["title"],
                "summary": summary,
                "link": article["link"],
                "embedding": embedding[0]  # Since we passed one string
            })

    return embedded_data

def save_embeddings(data, output_file="semantic_cache/news_embeddings.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    articles = load_news_data()
    embedder = Embedder()
    embedded_data = embed_news_articles(articles, embedder)
    save_embeddings(embedded_data)
    print("✅ Embedding complete and saved.")
