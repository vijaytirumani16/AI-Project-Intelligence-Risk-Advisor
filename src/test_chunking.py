from document_ingestion import read_document
from chunking import chunk_text


file_path = "../data/sample_documents/project_notes.txt"

text = read_document(file_path)

chunks = chunk_text(text)

print("Number of chunks:", len(chunks))
print("-" * 50)

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)
    print("-" * 50)