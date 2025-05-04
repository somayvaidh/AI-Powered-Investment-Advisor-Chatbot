import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Constants
EMBEDDING_FILE = "semantic_cache/news_embeddings.json"
INDEX_FILE = "vector_store/news_faiss.index"
MODEL_NAME = "all-MiniLM-L6-v2"

class NewsVectorSearch:
    def __init__(self, model_name=MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        self.embeddings = []
        self.metadata = []
        self.index = None
        self.load_embeddings()

    def load_embeddings(self, path=EMBEDDING_FILE):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.metadata = data
        self.embeddings = np.array([item["embedding"] for item in data], dtype="float32")
    
        print("✅ Loaded embeddings.")
        print("Embedding shape:", self.embeddings.shape)  # (num_articles, 384)
        print("Sample metadata:", self.metadata[0])       # Check that each item has useful content



    def build_index(self):
        dim = self.embeddings.shape[1]
        print("🧠 Embedding dimension:", dim)
    
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        print("📦 Added vectors to index:", self.index.ntotal)

        faiss.write_index(self.index, INDEX_FILE)
        print("✅ FAISS index built and saved.")


    def load_index(self):
        self.index = faiss.read_index(INDEX_FILE)
        print("✅ FAISS index loaded.")
    
    # Ensure metadata is also loaded
        if not self.metadata:
            self.load_embeddings()

    def query(self, user_text, top_k=5):
        query_embedding = self.model.encode([user_text])[0].astype("float32")
        print("🔎 Query embedding shape:", query_embedding.shape)

        D, I = self.index.search(np.array([query_embedding]), top_k)
        print("📏 Distances:", D)
        print("🆔 Indices:", I)

        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
               results.append(self.metadata[idx])
        return results


if __name__ == "__main__":
    search_engine = NewsVectorSearch()
    search_engine.load_embeddings()
    search_engine.build_index()

    query_text = "360 ONE WAM Ltd performance"
    print(f"\n🔍 Query: {query_text}")
    results = search_engine.query(query_text)
    
    if results:
        for res in results:
            print("✅ Match:", res.get("title", "No title"), "-", res.get("summary", "")[:100])
    else:
        print("❌ No relevant articles found.")

    