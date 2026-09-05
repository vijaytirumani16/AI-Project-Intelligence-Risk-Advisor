from multi_document_chunking import process_and_chunk_documents
from embeddings import create_embeddings
from vector_store import create_vector_store


data_folder = "../data/sample_documents"


print("Processing documents...")

chunks = process_and_chunk_documents(data_folder)

print("Number of chunks:", len(chunks))


chunk_texts = [
    chunk["text"]
    for chunk in chunks
]


print("\nCreating embeddings...")

embeddings = create_embeddings(chunk_texts)

print("Number of embeddings:", len(embeddings))


print("\nCreating vector store...")

collection = create_vector_store(
    chunks,
    embeddings
)


print("Vector store created successfully!")

print(
    "Number of documents stored:",
    collection.count()
)