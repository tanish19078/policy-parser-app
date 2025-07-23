from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Load local embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector store
def create_vector_store(chunks, metadata=None, index_path="vectorstore/index"):
    docs = []
    for i, chunk in enumerate(chunks):
        meta = metadata[i] if metadata and i < len(metadata) else {}
        docs.append(Document(page_content=chunk, metadata=meta))

    vectorstore = FAISS.from_documents(docs, embedding_model)
    vectorstore.save_local(index_path)
    return vectorstore

# Load existing index
def load_vector_store(index_path="vectorstore/index"):
    return FAISS.load_local(index_path, embedding_model)
