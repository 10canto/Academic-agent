"""
ingest.py - Load a PDF, chunk it, embed it, and store in Chroma vector database

This script runs ONCE per PDF to prepare it for question answering.
It extracts text from the PDF, splits it into chunks, and stores embeddings
in a local Chroma database for later retrieval.
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ============================================================================
# CONFIGURATION - Change these if needed
# ============================================================================
PDF_PATH = "data/sample.pdf"  # Path to your PDF file
CHROMA_DB_DIR = "chroma_db"   # Where to save the vector database
CHUNK_SIZE = 500              # Characters per chunk
CHUNK_OVERLAP = 50            # Overlap between chunks (helps preserve context)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # HuggingFace model

# ============================================================================
# STEP 1: Load the PDF
# ============================================================================
print("=" * 70)
print("STEP 1: Loading PDF...")
print("=" * 70)

# PyPDFLoader reads the PDF and extracts text from each page
# It automatically creates one Document object per page
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"✓ Loaded {len(documents)} pages from '{PDF_PATH}'")

# Show a preview of the first page to verify extraction worked
if documents:
    first_page_text = documents[0].page_content
    print(f"\nPreview of first page (first 300 characters):")
    print("-" * 70)
    print(first_page_text[:300])
    print("-" * 70)
else:
    print("⚠ WARNING: No text extracted! Your PDF might be scanned or empty.")
    exit(1)

# ============================================================================
# STEP 2: Split the text into chunks
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: Splitting text into chunks...")
print("=" * 70)

# RecursiveCharacterTextSplitter tries to split on paragraphs, then sentences,
# then words - this preserves meaning better than hard character cuts
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,  # Use character count
    add_start_index=True,  # Helps track where chunks came from
)

# Split all documents into smaller chunks
# Each chunk keeps metadata like page number
chunks = text_splitter.split_documents(documents)

print(f"✓ Created {len(chunks)} chunks from {len(documents)} pages")
print(f"  (Chunk size: {CHUNK_SIZE} chars, overlap: {CHUNK_OVERLAP} chars)")

# ============================================================================
# STEP 3: Create embeddings and store in Chroma
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: Creating embeddings and storing in Chroma...")
print("=" * 70)
print(f"Using embedding model: {EMBEDDING_MODEL}")
print("(This may take a minute on first run - downloading model...)")

# Initialize the embedding model
# This converts text into 384-dimensional vectors for semantic search
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'},  # Use 'cuda' if you have GPU
    encode_kwargs={'normalize_embeddings': True}  # Helps with similarity search
)

# Delete existing database if it exists (clean slate)
if os.path.exists(CHROMA_DB_DIR):
    print(f"⚠ Deleting existing database at '{CHROMA_DB_DIR}'...")
    import shutil
    shutil.rmtree(CHROMA_DB_DIR)

# Create Chroma database from documents
# Chroma automatically embeds each chunk and stores it with metadata
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DB_DIR  # Save to disk (not just RAM)
)

print(f"✓ Successfully stored {len(chunks)} chunks in Chroma database")
print(f"  Database saved to: {CHROMA_DB_DIR}/")

# ============================================================================
# DONE
# ============================================================================
print("\n" + "=" * 70)
print("✓ INGESTION COMPLETE!")
print("=" * 70)
print(f"Total pages processed: {len(documents)}")
print(f"Total chunks created: {len(chunks)}")
print(f"Vector database location: {CHROMA_DB_DIR}/")
print("\nYou can now run 'python src/query.py' to ask questions!")
print("=" * 70)
