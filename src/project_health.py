from rag_pipeline import ask_question


def calculate_project_health():
    """
    Analyze project health using the uploaded project documents.

    The health assessment includes:
    1. Scope Clarity
    2. Timeline Risk
    3. Blocker Count
    4. Overall Health Score
    """

    question = """
Analyze the uploaded project documents and generate a project health
assessment based ONLY on information contained in those documents.

Evaluate the following dimensions:

1. SCOPE CLARITY
   - Assess how clearly the project goals, deliverables, and scope are
     defined in the documents.
   - Provide a score from 0 to 100.
   - Explain the reason for the score using document evidence.

2. TIMELINE RISK
   - Assess the level of risk to the project timeline based on the
     documented project status, risks, delays, and schedule information.
   - Provide a score from 0 to 100 where:
       100 = low timeline risk / healthy timeline
       0 = very high timeline risk
   - Explain the reason for the score using document evidence.

3. BLOCKER COUNT
   - Identify the number of currently documented blockers.
   - List the blockers found in the documents.
   - If no blockers are explicitly documented, state:
     "No explicit blockers found in the documents."

4. OVERALL PROJECT HEALTH
   - Generate an overall health score from 0 to 100.
   - Consider scope clarity, timeline risk, and blocker situation.
   - Explain how the overall score was determined.

Use the following output structure:

PROJECT HEALTH SCORE
Overall Score: XX/100

1. Scope Clarity
Score: XX/100
Evidence:
...

2. Timeline Risk
Score: XX/100
Evidence:
...

3. Blocker Count
Count: X
Blockers:
...

4. Overall Assessment
...

IMPORTANT INSTRUCTIONS:

- Use ONLY information from the uploaded project documents.
- Do not invent project information, blockers, deadlines, or risks.
- Do not assume that missing information means the project is healthy.
- Clearly state when information is not specified in the documents.
- Keep the assessment structured and easy to understand.
"""

    health_assessment = ask_question(question)

    return health_assessment