import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embeddings import get_embedding_model
from src.vectorstore import load_vectorstore
from src.retriever import retrieve_relevant_chunks
from src.generator import generate_answer

embedding_model = get_embedding_model()
vectorstore = load_vectorstore(embedding_model, persist_directory="chroma_db")

queries = [
    "What is a vector in R programming?",
    "What is the attendance policy for exams?"
]

for query in queries:
    retrieved_docs = retrieve_relevant_chunks(query, vectorstore, k=3)
    start_time = time.time()
    answer = generate_answer(query, retrieved_docs)
    end_time = time.time()
    print(f"\n=== Query: {query} ===")
    print(f"ANSWER: {answer}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
