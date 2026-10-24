# Retrieval functions - finds relevant chunks from the vector database

from typing import List
from langchain_core.documents import Document


def retrieve_relevant_chunks(query, vectorstore, k=3):
    """
    Retrieve the k most relevant document chunks for a given query.
    
    Args:
        query: The search query string
        vectorstore: A Chroma vectorstore object
        k: Number of most relevant chunks to retrieve (default: 3)
        
    Returns:
        List of Document objects (the k most similar chunks)
    """
    results = vectorstore.similarity_search(query, k=k)
    
    return results
