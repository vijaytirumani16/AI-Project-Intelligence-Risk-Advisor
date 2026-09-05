from retrieval import search_documents
from llm import generate_response


def ask_question(question):

    results = search_documents(question)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    prompt = f"""
You are an AI assistant for an Enterprise Project Intelligence
and Risk Management Platform.

Answer the user's question using ONLY the project document
information provided below.

Project Document Information:
{context}

User Question:
{question}

Provide a clear and concise answer.
"""

    response = generate_response(prompt)

    return response