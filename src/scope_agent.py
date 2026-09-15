from rag_pipeline import ask_question


def extract_scope_and_deliverables():
    """
    Extract project scope and deliverable information
    from the uploaded project documents.
    """

    question = """
Analyze the uploaded project documents and extract the following
project scope and deliverable information.

1. Project Goals
   - Identify the main objectives or goals of the project.

2. Deliverables
   - Identify the major deliverables or outputs expected from the project.

3. Milestones
   - Identify any milestones mentioned in the documents.

4. Timeline
   - Identify dates, durations, deadlines, or schedule information.

5. Responsibilities
   - Identify people, teams, or roles responsible for project activities
     when explicitly mentioned.

Important instructions:
- Use ONLY information found in the uploaded project documents.
- Do not invent missing information.
- If a category is not available, state "Not specified in the documents".
- Keep the answer structured and clear.
"""

    analysis = ask_question(question)

    return analysis