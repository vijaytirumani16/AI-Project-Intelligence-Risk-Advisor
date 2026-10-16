from sentence_transformers import SentenceTransformer

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedding_model


def generate_embeddings(texts):
    model = get_embedding_model()
    return model.encode(texts)


def create_embeddings(texts):
    return generate_embeddings(texts)