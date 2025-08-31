from deepassert.diff_report.report_generator import generate_diff_report


def test_generate_diff_report__no_diff():
    d1 = {
        "a": 1,
        "b": 2,
        "c": None,
        "d": "d-value1",
        "e": {"e-nested-value": "e-nested-value1"},
    }

    # d2 = {
    #     "a": 1,
    #     "b": ANY_BUT_NONE,
    #     "c": ANY,
    #     "d": "d-value2",
    #     "e": {"e-nested-value": "e-nested-value2"},
    # }

    assert generate_diff_report(d1, d1) == ""
