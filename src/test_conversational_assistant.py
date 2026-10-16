from conversational_assistant import ask_project_assistant


def test_conversational_assistant():
    questions = [
        "What are our biggest risks?",
        "Are we on track?",
        "What action items are currently pending?"
    ]

    print("\n" + "=" * 70)
    print("CONVERSATIONAL PROJECT INTELLIGENCE ASSISTANT")
    print("=" * 70)

    for question in questions:

        print("\n" + "-" * 70)
        print(f"QUESTION: {question}")
        print("-" * 70)

        answer = ask_project_assistant(question)

        assert answer is not None
        assert isinstance(answer, str)
        assert len(answer.strip()) > 0

        print("\nANSWER:")
        print(answer)

    print("\n" + "=" * 70)
    print("CONVERSATIONAL ASSISTANT TEST COMPLETED")
    print("=" * 70)