from retrieval import search_documents


query = "What is the risk in the project?"

results = search_documents(query)

print("Query:")
print(query)

print("\nRetrieved Documents:")
print("-" * 50)

for document in results["documents"][0]:
    print(document)
    print("-" * 50)