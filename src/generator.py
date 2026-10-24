# LLM call for answer generation - handles Ollama interactions and prompt formatting

from langchain_ollama import OllamaLLM
from typing import List
from langchain_core.documents import Document


def generate_answer(query, retrieved_docs, model_name="qwen2.5:7b"):
    """
    Generate an answer to a query using retrieved document chunks and Ollama LLM.
    
    Args:
        query: The user's question string
        retrieved_docs: List of Document objects retrieved from vectorstore
        model_name: Name of the Ollama model to use (default: "qwen3.5:9b")
        
    Returns:
        Generated answer as a string
    """
    # Build context from retrieved documents with page numbers
    context_parts = []
    for doc in retrieved_docs:
        page_num = doc.metadata.get('page', 'unknown')
        content = doc.page_content
        context_parts.append(f"[Page {page_num}]: {content}")
    
    context = "\n\n".join(context_parts)
    
    # Build the prompt
    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context from a document.

RULES:
1. Answer the question using ONLY the context below
2. If the answer is not in the context, say "I don't have enough information in this document to answer that."
3. Do NOT use any outside knowledge
4. Always cite the page number(s) you used (e.g., "According to page 3...")
5. Be concise and direct

Context from the document:
{context}

Question: {query}

Answer:"""
    
    # Initialize Ollama LLM
    llm = OllamaLLM(
        model=model_name,
        temperature=0.1
    )
    
    # Generate answer
    answer = llm.invoke(prompt)
    
    return answer
