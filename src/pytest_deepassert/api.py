from typing import Any

from pytest_deepassert import diff_report


def equal(left: Any, right: Any) -> None:
    """
    Assert that two objects are equal.
    In case of inequality, a detailed diff report is generated for an assertion.

    Args:
        left: The left object.
        right: The right object.
    """
    assert left == right, diff_report.format_diff_report_lines(
        diff_report.generate_diff_report_lines(left, right) or []
    )
