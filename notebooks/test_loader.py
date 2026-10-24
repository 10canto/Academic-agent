import sys
import os

# Add the parent directory to Python path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.loader import load_pdf

docs = load_pdf(r"C:\Users\Anto\Downloads\IDS Unit 3.1.pdf")  # use your actual file path

print(type(docs))

print(len(docs))

print(type(docs[0]))

print(docs[0].page_content[:300])

print(docs[0].metadata)
