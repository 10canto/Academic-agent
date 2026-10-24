import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_pdf
from src.chunker import chunk_documents

docs = load_pdf("C:\\Users\\Anto\\Downloads\\IDS Unit 3.1.pdf")
chunks = chunk_documents(docs)

print(type(chunks))
print(len(chunks))
print("---- First chunk ----")
print(chunks[0].page_content)
print(chunks[0].metadata)
print("---- Second chunk ----")
print(chunks[1].page_content)

print("---- Third chunk ----")
print(chunks[2].page_content)