import sys
import os

# Add the parent directory to sys.path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_pdf
from src.chunker import chunk_documents
from src.embeddings import get_embedding_model
from src.vectorstore import create_vectorstore, load_vectorstore

# Step 1: Load the PDF
print("Loading PDF...")
docs = load_pdf(r"C:\Users\Anto\Downloads\IDS Unit 3.1.pdf")
print(f"Loaded {len(docs)} pages")

# Step 2: Chunk the documents
print("\nChunking documents...")
chunks = chunk_documents(docs)
print(f"Created {len(chunks)} chunks")

# Step 3: Get the embedding model
print("\nInitializing embedding model...")
embedding_model = get_embedding_model()
print("Embedding model ready")

# Step 4: Create vectorstore
print("\nCreating vectorstore...")
vectorstore = create_vectorstore(chunks, embedding_model, persist_directory="chroma_db")
print(f"Vectorstore chunk count: {vectorstore._collection.count()}")

# Step 5: Load vectorstore back
print("\nLoading vectorstore fresh...")
loaded_vectorstore = load_vectorstore(embedding_model, persist_directory="chroma_db")
print(f"Loaded vectorstore chunk count: {loaded_vectorstore._collection.count()}")

print("\n✓ Test complete!")
