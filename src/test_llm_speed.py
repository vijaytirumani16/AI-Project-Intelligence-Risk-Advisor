import time

from llm import generate_response


prompt = "Explain RAG in one simple sentence."


start_time = time.perf_counter()

response = generate_response(prompt)

end_time = time.perf_counter()

elapsed_time = end_time - start_time

print("\n" + "=" * 50)
print("LLM SPEED TEST")
print("=" * 50)

print(f"\nResponse:")
print(response)

print(f"\nResponse time: {elapsed_time:.2f} seconds")

print("\n" + "=" * 50)