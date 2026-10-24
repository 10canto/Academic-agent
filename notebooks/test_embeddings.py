import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.embeddings import get_embedding_model

embedding_model = get_embedding_model()

test_vector = embedding_model.embed_query("What is the attendance policy?")

print(type(test_vector))
print(len(test_vector))
print(test_vector[:5])
