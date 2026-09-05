from document_ingestion import read_document
from chunking import chunk_text
from embeddings import create_embeddings


file_path = "../data/sample_documents/project_notes.txt"

# Read the document
text = read_document(file_path)

# Split text into chunks
chunks = chunk_text(text)

# Create embeddings
embeddings = create_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))

print("\nEmbedding vector:")
print(embeddings[0])