from llm import generate_response


prompt = "Explain project risk management in two simple sentences."

response = generate_response(prompt)

print("Gemini Response:")
print("-" * 50)
print(response)