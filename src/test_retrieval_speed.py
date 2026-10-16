import time

from retrieval import search_documents


question = "What are our biggest project risks?"


print("\n" + "=" * 50)
print("RAG RETRIEVAL SPEED TEST")
print("=" * 50)


print("\nFirst retrieval:")

start_time = time.perf_counter()

results = search_documents(question)

end_time = time.perf_counter()

first_time = end_time - start_time

print(f"Retrieved chunks: {len(results['documents'][0])}")
print(f"Retrieval time: {first_time:.2f} seconds")


print("\nSecond retrieval:")

start_time = time.perf_counter()

results = search_documents(question)

end_time = time.perf_counter()

second_time = end_time - start_time

print(f"Retrieved chunks: {len(results['documents'][0])}")
print(f"Retrieval time: {second_time:.2f} seconds")


print("\n" + "=" * 50)
print("RESULT")
print("=" * 50)

print(f"First retrieval:  {first_time:.2f} seconds")
print(f"Second retrieval: {second_time:.2f} seconds")