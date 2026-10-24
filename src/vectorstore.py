# Chroma setup and retrieval functions - manages vector database operations

from langchain_community.vectorstores import Chroma
from typing import List
from langchain_core.documents import Document


def create_vectorstore(chunks, embedding_model, persist_directory="chroma_db"):
    """
    Create a Chroma vector store from document chunks.
    
    Args:
        chunks: List of Document objects (chunked text)
        embedding_model: Embedding model instance (e.g., HuggingFaceEmbeddings)
        persist_directory: Directory to save the vector store
        
    Returns:
        Chroma vectorstore object
    """
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    print(f"✓ Stored {len(chunks)} chunks in Chroma vector store at '{persist_directory}/'")
    
    return vectorstore


def load_vectorstore(embedding_model, persist_directory="chroma_db"):
    """
    Load an existing Chroma vector store from disk.
    
    Args:
        embedding_model: Embedding model instance (must match the one used during creation)
        persist_directory: Directory where the vector store is saved
        
    Returns:
        Chroma vectorstore object
    """
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    
    return vectorstore
