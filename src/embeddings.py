# Embedding model setup - initializes and configures the sentence transformer

from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Initialize and return a HuggingFace embedding model.
    
    Args:
        model_name: Name of the sentence-transformers model to use
        
    Returns:
        HuggingFaceEmbeddings instance
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    return embeddings
