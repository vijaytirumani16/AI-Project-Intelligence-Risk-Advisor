from conversational_assistant import ask_project_assistant


def test_conversational_accuracy_validation():

    validation_cases = [
        {
            "question": "What are our biggest risks?",
            "expected_keywords": [
                "document processing",
                "RAG pipeline"
            ]
        },
        {
            "question": "What action items are currently pending?",
            "expected_keywords": [
                "document ingestion",
                "testing"
            ]
        },
        {
            "question": "Are there any explicit blockers?",
            "expected_keywords": [
                "no explicit blocker",
                "no blockers",
                "information is not specified"
            ]
        }
    ]

    print("\n" + "=" * 70)
    print("CONVERSATIONAL ASSISTANT ACCURACY VALIDATION")
    print("=" * 70)

    passed = 0

    for index, case in enumerate(validation_cases, start=1):

        print("\n" + "-" * 70)
        print(f"VALIDATION CASE {index}")
        print("-" * 70)

        print(f"Question: {case['question']}")

        answer = ask_project_assistant(case["question"])

        assert answer is not None
        assert isinstance(answer, str)
        assert len(answer.strip()) > 0

        print("\nAnswer:")
        print(answer)

        answer_lower = answer.lower()

        matched_keywords = [
            keyword
            for keyword in case["expected_keywords"]
            if keyword.lower() in answer_lower
        ]

        if matched_keywords:
            print("\nResult: PASS")
            print(f"Matched evidence: {matched_keywords}")
            passed += 1
        else:
            print("\nResult: REVIEW")
            print(f"Expected evidence: {case['expected_keywords']}")

    print("\n" + "=" * 70)
    print(f"VALIDATION SUMMARY: {passed}/{len(validation_cases)} CASES PASSED")
    print("=" * 70)

    assert passed == len(validation_cases), (
        f"Only {passed}/{len(validation_cases)} validation cases passed."
    )