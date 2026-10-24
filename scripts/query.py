"""
query.py - Ask questions about your PDF and get answers from the RAG system

This script loads the Chroma database created by ingest.py, takes your questions,
retrieves relevant chunks, and uses Ollama to generate answers based ONLY on
the document content.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ============================================================================
# CONFIGURATION - Change these if needed
# ============================================================================
CHROMA_DB_DIR = "chroma_db"   # Where your vector database is stored
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Must match ingest.py!
OLLAMA_MODEL = "llama3.1:8b"  # Change to "phi3" or other model if needed
TOP_K_CHUNKS = 4              # How many chunks to retrieve per question
LLM_TEMPERATURE = 0.1         # Lower = more factual, higher = more creative

# ============================================================================
# STEP 1: Load the Chroma vector database
# ============================================================================
print("=" * 70)
print("LOADING RAG SYSTEM...")
print("=" * 70)

# Initialize the SAME embedding model used during ingestion
# If you use a different model, you'll get dimension mismatch errors!
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

print(f"✓ Loading vector database from '{CHROMA_DB_DIR}'...")

# Load the existing Chroma database
vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)

# Create a retriever that will find the most similar chunks
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K_CHUNKS}  # Get top K most relevant chunks
)

print(f"✓ Vector database loaded successfully")

# ============================================================================
# STEP 2: Set up the Ollama LLM
# ============================================================================
print(f"✓ Connecting to Ollama (model: {OLLAMA_MODEL})...")

# Initialize Ollama - make sure Ollama is running!
# Run 'ollama serve' in another terminal if you get connection errors
llm = OllamaLLM(
    model=OLLAMA_MODEL,
    temperature=LLM_TEMPERATURE  # Low temp for factual answers
)

print(f"✓ Ollama connection established")

# ============================================================================
# STEP 3: Create the RAG prompt template
# ============================================================================
# This prompt instructs the LLM to ONLY use the provided context
# and to cite page numbers. This reduces hallucination.
prompt_template = """You are a helpful assistant that answers questions based ONLY on the provided context from a document.

RULES:
1. Answer the question using ONLY the context below
2. If the answer is not in the context, say "I don't have enough information in this document to answer that."
3. Do NOT use any outside knowledge
4. Always cite the page number(s) you used (e.g., "According to page 3...")
5. Be concise and direct

Context from the document:
{context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# ============================================================================
# STEP 4: Main question-answering loop
# ============================================================================
print("\n" + "=" * 70)
print("RAG SYSTEM READY!")
print("=" * 70)
print(f"Model: {OLLAMA_MODEL}")
print(f"Retrieving top {TOP_K_CHUNKS} chunks per question")
print("Type your question and press Enter. Type 'exit' to quit.")
print("=" * 70 + "\n")

while True:
    # Get user question
    question = input("Your question: ").strip()
    
    if question.lower() in ['exit', 'quit', 'q']:
        print("\n👋 Goodbye!")
        break
    
    if not question:
        print("⚠ Please enter a question.\n")
        continue
    
    print("\n" + "-" * 70)
    print("RETRIEVING RELEVANT CHUNKS...")
    print("-" * 70)
    
    # Retrieve the most relevant chunks
    retrieved_docs = retriever.get_relevant_documents(question)
    
    if not retrieved_docs:
        print("⚠ No relevant chunks found in the database.\n")
        continue
    
    # Show what was retrieved (for debugging/verification)
    print(f"Found {len(retrieved_docs)} relevant chunks:\n")
    for i, doc in enumerate(retrieved_docs, 1):
        page_num = doc.metadata.get('page', 'unknown')
        preview = doc.page_content[:150].replace('\n', ' ')
        print(f"  [{i}] Page {page_num}: {preview}...")
    
    print("\n" + "-" * 70)
    print("GENERATING ANSWER...")
    print("-" * 70)
    
    # Build the context from retrieved chunks
    context = "\n\n".join([
        f"[Page {doc.metadata.get('page', 'unknown')}]: {doc.page_content}"
        for doc in retrieved_docs
    ])
    
    # Format the prompt with context and question
    formatted_prompt = PROMPT.format(context=context, question=question)
    
    # Get answer from Ollama
    try:
        answer = llm.invoke(formatted_prompt)
        
        print("\n📝 ANSWER:")
        print("=" * 70)
        print(answer.strip())
        print("=" * 70)
        
        # Show which pages were available for citation
        pages = sorted(set(doc.metadata.get('page', 'unknown') for doc in retrieved_docs))
        print(f"\n📄 Chunks retrieved from pages: {', '.join(map(str, pages))}")
        
    except Exception as e:
        print(f"\n❌ ERROR calling Ollama: {e}")
        print("Make sure Ollama is running ('ollama serve' in another terminal)")
    
    print("\n" + "=" * 70 + "\n")

print("\nSession ended.")
