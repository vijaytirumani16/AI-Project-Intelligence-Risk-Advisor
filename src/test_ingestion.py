from document_ingestion import read_document


file_path = "../data/sample_documents/project_summary.pdf"

text = read_document(file_path)

print("PDF Document Content:")
print("-" * 50)
print(text)