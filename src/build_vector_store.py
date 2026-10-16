
from pathlib import Path

from multi_document_chunking import process_and_chunk_documents
from embeddings import create_embeddings
from vector_store import create_vector_store


# Resolve the sample documents directory relative to the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data" / "sample_documents"


def main():
    print("Processing documents...")

    if not DATA_FOLDER.exists():
        raise FileNotFoundError(
            f"Sample documents folder not found: {DATA_FOLDER}"
        )

    chunks = process_and_chunk_documents(str(DATA_FOLDER))

    print("Number of chunks:", len(chunks))

    if not chunks:
        print("No document chunks found. Nothing to index.")
        return

    # Generate embeddings from text only.
    chunk_texts = [
        chunk["text"] if isinstance(chunk, dict) else str(chunk)
        for chunk in chunks
    ]

    print("\nCreating embeddings...")

    embeddings = create_embeddings(chunk_texts)

    print("Number of embeddings:", len(embeddings))

    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk/embedding mismatch: {len(chunks)} chunks, "
            f"{len(embeddings)} embeddings."
        )

    print("\nAdding documents to the vector store...")

    collection = create_vector_store(chunks, embeddings)

    print("\nVector store operation completed successfully!")
    print("Total chunks stored:", collection.count())


if __name__ == "__main__":
    main()
