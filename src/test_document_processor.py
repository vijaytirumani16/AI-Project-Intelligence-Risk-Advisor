from document_processor import process_documents


documents = process_documents("../data/sample_documents")

print("Number of documents:", len(documents))

print("\nDOCUMENT CONTENTS")
print("=" * 50)

for index, document in enumerate(documents):

    print(f"\nDocument {index + 1}:")
    print("-" * 50)

    print(document)