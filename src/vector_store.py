import chromadb
from pathlib import Path


def create_vector_store(chunks, embeddings):
    """
    Store text chunks, embeddings, and metadata in ChromaDB.
    """

    project_path = Path(__file__).resolve().parent.parent

    database_path = project_path / "vector_store"

    client = chromadb.PersistentClient(
        path=str(database_path)
    )

    # Delete the old collection to avoid duplicates
    try:
        client.delete_collection(
            name="project_documents"
        )
    except:
        pass


    collection = client.get_or_create_collection(
        name="project_documents"
    )


    documents = [
        chunk["text"]
        for chunk in chunks
    ]


    metadatas = [
        {
            "source": chunk["source"]
        }
        for chunk in chunks
    ]


    ids = [
        f"chunk_{index}"
        for index in range(len(chunks))
    ]


    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    return collection