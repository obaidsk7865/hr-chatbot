# embed.py
import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm
import pickle

MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
INDEX_PATH = "faiss_index.bin"
META_PATH = "index_meta.pkl"
KB_PATH = "hr_faq.json"

def load_kb(kb_path):
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_embeddings(kb, model_name=MODEL_NAME):
    model = SentenceTransformer(model_name)
    texts = []
    metas = []
    for i, item in enumerate(kb):
        q = item.get("question","")
        a = item.get("answer","")
        text = (q + " " + a).strip()
        texts.append(text)
        metas.append({"id": i, "question": q, "answer": a})
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embeddings, metas

def build_faiss(embeddings, dim):
    # L2-normalize recommended for cosine similarity with inner product
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dim)  # inner product on normalized vectors = cosine similarity
    index.add(embeddings)
    return index

def save_index(index, meta, index_path=INDEX_PATH, meta_path=META_PATH):
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(meta, f)
    print("Saved index and metadata.")

def main():
    kb = load_kb(KB_PATH)
    embeddings, meta = build_embeddings(kb)
    dim = embeddings.shape[1]
    index = build_faiss(embeddings, dim)
    save_index(index, meta)

if __name__ == "__main__":
    main()
