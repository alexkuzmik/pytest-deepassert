from typing import Any, List

from . import compare_helpers_deepdiff_operator
import deepdiff
import logging


LOGGER = logging.getLogger(__name__)


def generate_diff_report_lines(
    expected: Any, actual: Any, verbose_level: int = 2, **kwargs: Any
) -> List[str]:
    try:
        custom_operator = (
            compare_helpers_deepdiff_operator.COMPARE_HELPERS_DEEPDIFF_OPERATOR
        )

        diff = deepdiff.DeepDiff(
            expected,
            actual,
            custom_operators=[custom_operator],
            verbose_level=verbose_level,
            **kwargs,
        )

        return diff.pretty().split("\n")
    except Exception:
        LOGGER.debug("Failed to generate diff report", exc_info=True)
        return []


def format_diff_report_lines(diff_report_lines: List[str]) -> str:
    result_lines: List[str] = []

    if len(diff_report_lines) == 0:
        return ""

    result_lines.append("")
    result_lines.append("DeepAssert detailed comparison:")

    for line in diff_report_lines:
        if line.strip():
            result_lines.append(f"    {line}")

    return "\n".join(result_lines)
