from rag_pipeline import ask_question


question = "What is the main risk in the project?"

answer = ask_question(question)

print("Question:")
print(question)

print("\nAI Answer:")
print("-" * 50)
print(answer)