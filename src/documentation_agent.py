from rag_pipeline import ask_question


def generate_project_documentation():
    """
    Generate project documentation from the uploaded project documents.

    The generated documentation includes:
    1. User Stories
    2. Risk Register
    3. Structured Action Items
    """

    question = """
Analyze the uploaded project documents and generate structured project
documentation based ONLY on the information contained in those documents.

Generate the following three sections:

1. USER STORIES

Create user stories for project activities, requirements, or work items
that are supported by the uploaded documents.

Use this format:

US-XXX:
As a [user/role],
I want [requirement/action],
so that [benefit/purpose].

Do not invent requirements that are not supported by the documents.

2. RISK REGISTER

Create a structured risk register using risks identified in the uploaded
documents.

For each risk provide:

- Risk ID
- Risk Description
- Impact
- Likelihood
- Risk Level
- Mitigation / Recommended Action

Only include risks supported by the project documents.

If impact, likelihood, or mitigation information is not available,
state "Not specified in the documents."

3. ACTION ITEMS

Create a structured list of pending or required project actions.

For each action provide:

- Action ID
- Action Description
- Responsible Person/Team
- Priority
- Status

Only use information explicitly supported by the documents.

If responsibility, priority, or status is not available,
state "Not specified in the documents."

IMPORTANT INSTRUCTIONS:

- Use ONLY information from the uploaded project documents.
- Do not invent project requirements, risks, responsibilities, dates,
  priorities, or actions.
- Clearly distinguish existing information from information that is
  not specified.
- If a section has no supported information, state:
  "Not specified in the documents."
- Keep the output structured and easy to read.
"""

    documentation = ask_question(question)

    return documentation