from vector_store import create_vector_store
from embeddings import create_embeddings
from multi_document_chunking import process_and_chunk_documents


data_folder = "../data/sample_documents"


print("Loading documents...")

chunks = process_and_chunk_documents(data_folder)


chunk_texts = [
    chunk["text"]
    for chunk in chunks
]


print("Creating embeddings...")

embeddings = create_embeddings(chunk_texts)


print("Loading vector store...")

collection = create_vector_store(
    chunks,
    embeddings
)


question = "What is the highest risk task?"


print("\nQuestion:")
print(question)


question_embedding = create_embeddings(
    [question]
)


results = collection.query(
    query_embeddings=question_embedding.tolist(),
    n_results=4
)


print("\nRetrieved Documents:")
print("=" * 50)


documents = results["documents"][0]
metadatas = results["metadatas"][0]


for document, metadata in zip(
    documents,
    metadatas
):

    print("Source:", metadata["source"])
    print()
    print(document)

    print("-" * 50)