# RAG System Version 1 - College Capstone Project

A simple command-line Retrieval-Augmented Generation (RAG) system that lets you ask questions about a PDF document and get answers grounded in that document.

## What is RAG?

RAG combines two things:
1. **Retrieval**: Find relevant chunks from your document using semantic search
2. **Generation**: Use an AI model to answer questions based on those chunks

This prevents the AI from hallucinating or making things up - it can only answer based on what's actually in your PDF.

---

## Prerequisites

Before you start, make sure you have:

1. **Python 3.10 or higher** installed
   - Check with: `python --version`

2. **Ollama installed and running**
   - Download from: https://ollama.ai
   - After installing, run: `ollama pull llama3.1:8b`
   - Start the server: `ollama serve` (keep this running in a separate terminal)

3. **A PDF file** to ask questions about
   - Place it at: `data/sample.pdf`
   - Works best with text-based PDFs (not scanned images)

---

## Setup Instructions

### Step 1: Install Python Dependencies

Open a terminal in this project folder and run:

```bash
pip install -r requirements.txt
```

This will install:
- **LangChain**: Framework for building RAG systems
- **ChromaDB**: Vector database to store document embeddings
- **sentence-transformers**: Converts text to embeddings (vectors)
- **pypdf**: Reads PDF files
- **langchain-ollama**: Connects to your local Ollama server

**First-time note**: The first run will download the embedding model (all-MiniLM-L6-v2, about 80MB). This is normal and only happens once.

---

### Step 2: Add Your PDF

Place your PDF file in the `data/` folder and name it `sample.pdf`:

```
data/sample.pdf
```

**Important**: This works best with text-based PDFs. If your PDF is a scanned image, the text extraction will fail (see Troubleshooting below).

---

### Step 3: Ingest the PDF (Run Once)

This step processes your PDF and stores it in the vector database:

```bash
python src/ingest.py
```

**What happens:**
1. Loads your PDF and extracts text from each page
2. Splits the text into chunks (500 characters each with 50 char overlap)
3. Converts each chunk into a vector embedding
4. Stores everything in `chroma_db/` folder

**Output**: You'll see the number of pages, chunks created, and a preview of the first page.

**Time**: Takes 1-3 minutes depending on PDF size.

---

### Step 4: Ask Questions (Run Repeatedly)

Now you can ask questions about your PDF:

```bash
python src/query.py
```

**What happens:**
1. Loads the vector database
2. Connects to Ollama
3. Starts an interactive loop where you can ask questions

**Example session:**
```
Your question: What is the main topic of this document?

RETRIEVING RELEVANT CHUNKS...
Found 4 relevant chunks:
  [1] Page 0: This document discusses...
  [2] Page 2: The primary focus is on...
  ...

GENERATING ANSWER...
📝 ANSWER:
According to page 0, the main topic of this document is...

📄 Chunks retrieved from pages: 0, 2, 3
```

Type `exit` to quit.

---

## How It Works (Simple Explanation)

1. **Ingest Phase** (`ingest.py`):
   - Your PDF is broken into small chunks
   - Each chunk is converted to a 384-number vector (embedding) that captures its meaning
   - These vectors are stored in ChromaDB with metadata (page number, etc.)

2. **Query Phase** (`query.py`):
   - Your question is also converted to a vector
   - ChromaDB finds the 4 most similar chunk vectors (semantic search)
   - Those chunks are given to Ollama as context
   - Ollama generates an answer using ONLY that context

---

## How Do I Know This Is Working?

Run these three tests:

### ✅ Test 1: Question with answer IN the document
Ask a question whose answer is clearly in your PDF.

**Expected result**: You get a correct answer with page citations.

**Example**: If your PDF is about Python programming, ask "What is a Python function?"

---

### ✅ Test 2: Question UNRELATED to the document
Ask something completely off-topic.

**Expected result**: The system says "I don't have enough information in this document to answer that." It should NOT make up an answer.

**Example**: If your PDF is about Python, ask "What is the capital of France?"

---

### ✅ Test 3: Swapping in a new PDF
1. Delete the old vector database: `rm -rf chroma_db/` (or manually delete the folder)
2. Replace `data/sample.pdf` with your new PDF
3. Re-run: `python src/ingest.py`
4. Run: `python src/query.py`

**Expected result**: Questions now work on the NEW document.

---

## Configuration Options

Want to change settings? Edit these variables at the top of each file:

### In `ingest.py`:
- `CHUNK_SIZE = 500`: Size of text chunks (smaller = more precise, larger = more context)
- `CHUNK_OVERLAP = 50`: Overlap between chunks (helps preserve meaning across boundaries)

### In `query.py`:
- `OLLAMA_MODEL = "llama3.1:8b"`: Change to `"phi3"` or any other Ollama model
- `TOP_K_CHUNKS = 4`: How many chunks to retrieve (more = more context but slower)
- `LLM_TEMPERATURE = 0.1`: 0.0 = very factual, 1.0 = more creative (keep low for RAG)

---

## Troubleshooting

### 🔴 Error: "Connection refused" or "Ollama not running"

**Problem**: The Ollama server isn't running.

**Fix**:
1. Open a new terminal
2. Run: `ollama serve`
3. Keep that terminal open
4. Try `query.py` again

**Check**: Visit http://localhost:11434 in a browser - you should see "Ollama is running"

---

### 🔴 Error: "Dimensionality mismatch" or "Embedding dimension does not match"

**Problem**: You changed the embedding model in `query.py` but the database was built with a different model.

**Fix**:
1. Delete the vector database: `rm -rf chroma_db/`
2. Make sure `EMBEDDING_MODEL` is the SAME in both `ingest.py` and `query.py`
3. Re-run: `python src/ingest.py`

**Why**: Each embedding model outputs different vector sizes. Once you create a database with one model, you must use that same model to query it.

---

### 🔴 Warning: "No text extracted! Your PDF might be scanned or empty."

**Problem**: Your PDF is likely a scanned image (not searchable text).

**Fix**:
1. Option A: Use a different PDF that has selectable text (test by trying to copy/paste text from it)
2. Option B: Use OCR to convert your scanned PDF to text first (tools: Adobe Acrobat, online OCR services)

**Check**: Open your PDF and try to select text with your mouse. If you can't select it, it's a scanned image.

---

### 🔴 Import errors or "ModuleNotFoundError"

**Problem**: Dependencies not installed correctly.

**Fix**:
1. Make sure you're in the project folder
2. Run: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.10+)

---

### 🔴 Answers seem generic or don't cite the document

**Problem**: The LLM might be ignoring the context.

**Fix**:
1. Check that chunks were actually retrieved (you should see them printed before the answer)
2. Try a more specific question
3. Lower the `LLM_TEMPERATURE` to 0.0 for more grounded answers
4. Try a different Ollama model (some are better at following instructions)

---

## Project Structure

```
COA capstone/
├── data/
│   └── sample.pdf          # Your PDF file (you provide this)
├── src/
│   ├── ingest.py           # Run once to process PDF
│   └── query.py            # Run to ask questions
├── chroma_db/              # Vector database (auto-created)
├── requirements.txt        # Python dependencies
└── README_v1.md           # This file
```

---

## Next Steps / Future Improvements

Once you have this working, you could:
- Add support for multiple PDFs
- Build a web interface instead of command-line
- Try different embedding models or LLMs
- Add a "chat history" so the LLM remembers previous questions
- Experiment with different chunk sizes and retrieval strategies

---

## Questions?

Common beginner questions:

**Q: Do I need an API key?**  
A: No! Everything runs locally (Ollama + HuggingFace embeddings).

**Q: Can I use GPT-4 or Claude instead of Ollama?**  
A: Yes, but you'll need to modify `query.py` to use their APIs and provide API keys.

**Q: How big can my PDF be?**  
A: Most PDFs work fine. Very large ones (500+ pages) may take 5-10 minutes to ingest.

**Q: Can I ask multiple questions without re-running ingest.py?**  
A: Yes! Run `ingest.py` once, then run `query.py` as many times as you want.

**Q: Does this work on Windows/Mac/Linux?**  
A: Yes, all platforms are supported.

---

**Good luck with your capstone project!** 🎓
