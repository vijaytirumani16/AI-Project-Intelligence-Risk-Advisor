from sentence_transformers import SentenceTransformer


def get_embedding_model():
    """
    Load and return the embedding model.
    """

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model


def create_embeddings(chunks):
    """
    Convert text chunks into numerical embeddings.
    """

    model = get_embedding_model()

    embeddings = model.encode(chunks)

    return embeddings