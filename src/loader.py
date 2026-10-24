# PDF loading functions - reads PDFs and extracts text

from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> List[Document]:
    """
    Load a PDF file and extract text from each page.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of Document objects, one per page, with page_content and metadata
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents
