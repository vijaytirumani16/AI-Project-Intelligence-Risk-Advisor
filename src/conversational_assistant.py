from rag_pipeline import ask_question


def ask_project_assistant(question):
    """
    Answer project-related questions using the uploaded
    project documents through the RAG pipeline.
    """
    return ask_question(question)