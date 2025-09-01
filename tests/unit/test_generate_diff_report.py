import pytest


def test_generate_diff_report__no_diff():
    d1 = {
        "a": 1,
        "b": 2,
        "c": None,
        "d": "d-value1",
        "e": {"e-nested-value": "e-nested-value1"},
    }

    d2 = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": "d-value2",
        "e": {"e-nested-value": "e-nested-value2"},
    }

    assert d1 == d2, "Some long assertion message to check if pytest assertion hook is still working"


if __name__ == "__main__":
    pytest.main()