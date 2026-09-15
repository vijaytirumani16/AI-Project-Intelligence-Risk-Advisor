from rag_pipeline import ask_question


def detect_risks_and_forecast_delivery():
    """
    Identify project risks, dependency gaps, delivery challenges,
    and possible delivery delays from the uploaded project documents.
    """

    question = """
Analyze the uploaded project documents specifically for project risks
and delivery forecasting.

Provide the following information:

1. Schedule Risks
   - Identify risks that could cause delays to the project schedule.
   - Include the evidence or situation described in the documents.

2. Dependency Gaps
   - Identify dependencies between tasks, modules, activities, or
     deliverables that may affect project progress.
   - Only identify dependencies explicitly supported by the documents.

3. Delivery Challenges
   - Identify current challenges that could affect successful project
     delivery.

4. Possible Delivery Delays
   - Identify whether the documents indicate a possibility of delay.
   - Explain the reason for the potential delay.

5. Risk Priority
   - Classify each identified risk as High, Medium, or Low when the
     documents provide enough information to support the classification.
   - Do not invent a priority when it cannot be determined.

Important instructions:
- Use ONLY information from the uploaded project documents.
- Do not invent risks, dependencies, dates, or project information.
- If information is not available, state:
  "Not specified in the documents."
- Clearly distinguish between an existing risk and a possible future risk.
- Give the answer in a clear and structured format.
"""

    analysis = ask_question(question)

    return analysis