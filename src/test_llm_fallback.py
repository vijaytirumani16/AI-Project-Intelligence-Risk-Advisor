from llm import generate_response

prompt = """
Explain what a RAG pipeline is in two simple sentences.
"""

print("\n===== MULTI-LLM FALLBACK TEST =====\n")

response = generate_response(prompt)

print("\n===== FINAL RESPONSE =====\n")
print(response)