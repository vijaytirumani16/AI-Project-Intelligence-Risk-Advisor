from documentation_agent import generate_project_documentation


def test_documentation_generation():
    result = generate_project_documentation()

    assert result is not None
    assert isinstance(result, str)
    assert len(result.strip()) > 0

    print("\n" + "=" * 70)
    print("DOCUMENTATION GENERATION AGENT")
    print("=" * 70)
    print("\n" + result)
    print("\n" + "=" * 70)
    print("DOCUMENTATION GENERATION TEST COMPLETED")
    print("=" * 70)