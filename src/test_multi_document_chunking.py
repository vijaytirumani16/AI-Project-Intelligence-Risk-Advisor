from multi_document_chunking import process_and_chunk_documents


chunks = process_and_chunk_documents("../data/sample_documents")

print("Total number of chunks:", len(chunks))

print("\nCHUNKS")
print("=" * 50)

for index, chunk in enumerate(chunks):

    print(f"\nChunk {index + 1}:")
    print("-" * 50)

    print(chunk)