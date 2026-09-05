from rag_pipeline import ask_question


def analyze_project():

    question = """
Analyze the project information and provide the following:

1. Project Status
2. Risks
3. Blockers
4. Action Items
5. Possible Delivery Delays

Give the answer in a clear and structured format.
"""

    analysis = ask_question(question)

    return analysis