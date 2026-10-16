from retrieval import search_documents
from llm import generate_response


def ask_question(question):
    """
    Answer a user question using only relevant information
    from the uploaded project documents.
    """

    results = search_documents(question)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return "The information is not specified in the uploaded project documents."

    # Build evidence with source information and retrieval distance.
    evidence_parts = []

    for index, document in enumerate(documents):
        source = "Unknown source"

        if index < len(metadatas) and metadatas[index]:
            source = metadatas[index].get("source", "Unknown source")

        distance = None

        if index < len(distances):
            distance = distances[index]

        evidence_parts.append(
            f"""
SOURCE: {source}
RETRIEVAL DISTANCE: {distance}

DOCUMENT CONTENT:
{document}
"""
        )

    evidence = "\n".join(evidence_parts)

    prompt = f"""
You are the Conversational Project Intelligence Assistant for an
Enterprise Project Intelligence and Risk Management Platform.

Your ONLY knowledge source is the project-document evidence provided
below.

USER QUESTION:
{question}

RETRIEVED PROJECT-DOCUMENT EVIDENCE:
{evidence}

Your task is to determine whether the retrieved evidence actually
contains information that is relevant to the user's question.

IMPORTANT RULES:

1. Answer ONLY from the retrieved project-document evidence.

2. First determine whether the evidence is relevant to the user's
   question.

3. If the evidence does NOT contain information relevant to the
   question, respond EXACTLY with:

The information is not specified in the uploaded project documents.

4. Do NOT answer unrelated general-knowledge questions.

5. Do NOT use outside knowledge.

6. Do NOT assume that retrieved documents are relevant simply because
   they were returned by the vector database.

7. For valid project questions, use the relevant evidence to provide
   a specific answer to the user's actual question.

8. For project-analysis questions such as:
   - Are we on track?
   - What are our biggest risks?
   - What could delay the project?
   - What are the current blockers?
   - What should we prioritize?

   you may reason from multiple facts in the evidence.

9. When making an inference, clearly indicate that it is an inference
   based on the uploaded project documents.

10. Never invent project facts, people, dates, statuses, risks,
    metrics, responsibilities, or other information.

11. Do not simply repeat the retrieved documents. Answer the user's
    actual question.

12. Keep the answer clear and concise.

Now answer the user's question.
"""

    return generate_response(prompt)