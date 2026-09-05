import chromadb
from pathlib import Path
from embeddings import get_embedding_model


def get_collection():
    """
    Connect to the existing ChromaDB collection.
    """

    project_path = Path(__file__).resolve().parent.parent

    database_path = project_path / "vector_store"

    client = chromadb.PersistentClient(
        path=str(database_path)
    )

    collection = client.get_collection(
        name="project_documents"
    )

    return collection


def search_documents(query, n_results=3):
    """
    Search for relevant document chunks.
    """

    collection = get_collection()

    model = get_embedding_model()

    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results