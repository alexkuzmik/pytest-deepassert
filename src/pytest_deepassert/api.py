from typing import Any

import pytest

from pytest_deepassert import diff_report


def equal(left: Any, right: Any, verbose_level: int = 2) -> None:
    """
    Assert that two objects are equal.
    In case of inequality, a detailed diff report is generated for an assertion.

    Args:
        left: The left object.
        right: The right object.
        verbose_level: The level of verbosity for the diff report.
    """
    __tracebackhide__ = True

    if left == right or right == left:
        # Check the equality from both sides to avoid unnecessary diff report generation
        # when one of the objects a special comparison helper type, for example mock.ANY or pytest.approx(...) instance.
        return None

    diff_message = diff_report.format_diff_report_lines(
        diff_report.generate_diff_report_lines(left, right, verbose_level=verbose_level)
        or []
    )
    pytest.fail(diff_message)
