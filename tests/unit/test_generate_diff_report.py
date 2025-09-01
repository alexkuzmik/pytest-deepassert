from pytest_deepassert import diff_report


def test_generate_diff_report__no_diff():
    d1 = {
        "a": 1,
        "b": 2,
        "c": None,
    }

    d2 = {
        "a": 1,
        "b": 42,
        "c": 100,
    }
    lines = diff_report.generate_diff_report_lines(d1, d2)
    assert len(lines) == 2
