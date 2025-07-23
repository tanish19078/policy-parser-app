import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Load MiniLM model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_vector_store(index_path="vectorstore/index/"):
    index_file = os.path.join(index_path, "faiss.index")
    meta_file = os.path.join(index_path, "metadata.pkl")

    if not os.path.exists(index_file) or not os.path.exists(meta_file):
        raise FileNotFoundError("FAISS index or metadata file not found.")

    index = faiss.read_index(index_file)
    with open(meta_file, "rb") as f:
        metadata = pickle.load(f)
    
    return index, metadata

def retrieve_top_k(query: str, k=5):
    # Embed query
    query_embedding = embedding_model.encode([query])
    
    # Load vector index and metadata
    index, metadata = load_vector_store()
    
    # Perform similarity search
    D, I = index.search(np.array(query_embedding).astype("float32"), k)
    
    results = []
    for i in I[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results
