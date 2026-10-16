from project_health import calculate_project_health


def test_project_health_scoring():
    result = calculate_project_health()

    assert result is not None
    assert isinstance(result, str)
    assert len(result.strip()) > 0

    print("\n" + "=" * 70)
    print("PROJECT HEALTH SCORING")
    print("=" * 70)
    print("\n" + result)
    print("\n" + "=" * 70)
    print("PROJECT HEALTH SCORING TEST COMPLETED")
    print("=" * 70)