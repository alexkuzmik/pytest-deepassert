import pytest
from typing import Any, Optional, List
from pytest_deepassert import diff_report
import _pytest.assertion.util


def pytest_addoption(parser):  # type: ignore
    """Add command line options for pytest-deepassert."""
    group = parser.getgroup("deepassert")
    group.addoption(
        "--deepassert",
        action="store_true",
        help="Enable deep assertion diffs from pytest-deepassert",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(
    config: pytest.Config, op: str, left: Any, right: Any
) -> Optional[List[str]]:
    """
    Custom hook that enhances pytest's assertion comparison output.

    Args:
        config: The pytest config object.
        op: The comparison operator as a string (e.g. '==', '!=').
        left: The left-hand side of the comparison.
        right: The right-hand side of the comparison.

    Returns:
        A list of strings representing the formatted comparison output,
        or None if not handled.
    """
    if not config.getoption("--deepassert"):
        return None

    if op != "==":
        return None

    if left == right or right == left:
        return None

    diff_lines = diff_report.generate_diff_report_lines(expected=left, actual=right)

    if len(diff_lines) == 0:
        return None

    result = []

    result.extend(diff_report.format_diff_report_lines(diff_lines).split("\n"))
    result.append("")

    standard_diff = _pytest.assertion.util.assertrepr_compare(config, op, left, right)

    if standard_diff:
        result.extend(standard_diff)
        result.append("")

    return result
