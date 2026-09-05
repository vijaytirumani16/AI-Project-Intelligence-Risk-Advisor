from document_ingestion import read_document
from chunking import chunk_text
from embeddings import create_embeddings
from vector_store import create_vector_store


file_path = "../data/sample_documents/project_notes.txt"

# Step 1: Read document
text = read_document(file_path)

# Step 2: Create chunks
chunks = chunk_text(text)

# Step 3: Create embeddings
embeddings = create_embeddings(chunks)

# Step 4: Store in ChromaDB
collection = create_vector_store(chunks, embeddings)

print("Vector store created successfully!")
print("Number of documents stored:", collection.count())