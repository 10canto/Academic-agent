# Text splitting functions - breaks documents into chunks for embedding

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document


def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    """
    Split documents into smaller chunks for embedding.
    
    Args:
        documents: List of Document objects to chunk
        chunk_size: Number of characters per chunk
        chunk_overlap: Number of overlapping characters between chunks
        
    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks
