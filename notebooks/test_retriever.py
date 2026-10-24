import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_pdf
from src.chunker import chunk_documents
from src.embeddings import get_embedding_model
from src.vectorstore import load_vectorstore
from src.retriever import retrieve_relevant_chunks

embedding_model = get_embedding_model()
vectorstore = load_vectorstore(embedding_model, persist_directory="chroma_db")

query = "What is the attendance policy for exams?"
results = retrieve_relevant_chunks(query, vectorstore, k=3)

print(f"Number of chunks retrieved: {len(results)}")
for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content[:300])
    print(doc.metadata)
