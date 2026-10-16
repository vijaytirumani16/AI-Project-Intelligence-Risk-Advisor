
import hashlib
from pathlib import Path

import chromadb


COLLECTION_NAME = "project_documents"


def create_vector_store(chunks, embeddings):
    """
    Persist document chunks in ChromaDB.

    - Keeps chunks belonging to other source files.
    - Replaces existing chunks when a source file is reprocessed.
    - Uses stable IDs to prevent duplicate chunks.
    - Preserves source filenames as metadata.
    """

    if not chunks:
        raise ValueError("No document chunks were provided.")

    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()
    else:
        embeddings = list(embeddings)

    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Received {len(chunks)} chunks but "
            f"{len(embeddings)} embeddings."
        )

    project_root = Path(__file__).resolve().parent.parent
    database_path = project_root / "vector_store"

    client = chromadb.PersistentClient(
        path=str(database_path)
    )

    # Never delete the entire collection.
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Prepare valid chunks and deduplicate repeated IDs.
    records = {}

    for chunk, embedding in zip(chunks, embeddings):
        if isinstance(chunk, dict):
            text = str(chunk.get("text", "")).strip()
            source = str(chunk.get("source", "unknown"))
        else:
            text = str(chunk).strip()
            source = "unknown"

        if not text:
            continue

        identity = f"{source}\0{text}".encode("utf-8")
        chunk_id = "chunk_" + hashlib.sha256(identity).hexdigest()

        records[chunk_id] = {
            "text": text,
            "source": source,
            "embedding": embedding,
        }

    if not records:
        raise ValueError("No valid text chunks were available.")

    # Only replace chunks for the source files being processed.
    sources_to_replace = sorted(
        {record["source"] for record in records.values()}
    )

    # Read the existing records for these sources so that if indexing
    # fails, we can attempt to restore the previous records.
    previous_records = []

    for source in sources_to_replace:
        existing = collection.get(
            where={"source": source},
            include=["documents", "metadatas", "embeddings"],
        )

        for index, existing_id in enumerate(existing["ids"]):
            previous_records.append({
                "id": existing_id,
                "document": existing["documents"][index],
                "metadata": existing["metadatas"][index],
                "embedding": existing["embeddings"][index],
            })

    # Replace the selected sources without affecting other files.
    try:
        for source in sources_to_replace:
            collection.delete(
                where={"source": source}
            )

        prepared = list(records.items())

        collection.upsert(
            ids=[item[0] for item in prepared],
            documents=[
                item[1]["text"] for item in prepared
            ],
            metadatas=[
                {"source": item[1]["source"]}
                for item in prepared
            ],
            embeddings=[
                item[1]["embedding"] for item in prepared
            ],
        )

    except Exception:
        # Best-effort restoration of the old records if indexing fails.
        try:
            for source in sources_to_replace:
                collection.delete(where={"source": source})

            if previous_records:
                collection.upsert(
                    ids=[
                        item["id"] for item in previous_records
                    ],
                    documents=[
                        item["document"] for item in previous_records
                    ],
                    metadatas=[
                        item["metadata"] for item in previous_records
                    ],
                    embeddings=[
                        item["embedding"] for item in previous_records
                    ],
                )
        except Exception as restore_error:
            print(
                "Warning: Could not fully restore previous records:",
                restore_error,
            )

        raise

    print(f"Processed {len(records)} unique chunks.")
    print(f"Updated sources: {', '.join(sources_to_replace)}")
    print(f"Total chunks in knowledge base: {collection.count()}")

    return collection
