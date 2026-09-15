from rag_pipeline import ask_question


def identify_blockers_and_action_items():
    """
    Identify blockers, pending decisions, unresolved issues,
    and action items from the uploaded project documents.
    """

    question = """
Analyze the uploaded project documents specifically for blockers
and action items.

Provide the following information:

1. Pending Decisions
   - Identify decisions that are still pending or need to be made.

2. Unresolved Issues
   - Identify issues or problems that are currently unresolved.

3. Blockers
   - Identify anything that is currently preventing or slowing
     project progress.

4. Action Items
   - Identify tasks or actions that need to be completed.

5. Assigned Responsibilities
   - Identify the person, team, or role assigned to each action item
     when explicitly mentioned in the documents.

Important instructions:
- Use ONLY information from the uploaded project documents.
- Do not invent decisions, issues, blockers, action items,
  responsibilities, or assignees.
- If information is not available, state:
  "Not specified in the documents."
- Clearly distinguish between completed actions and pending actions.
- Give the answer in a clear and structured format.
"""

    analysis = ask_question(question)

    return analysis