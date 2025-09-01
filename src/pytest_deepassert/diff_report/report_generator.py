from typing import Any, Optional, List

from . import compare_helpers_deepdiff_operator
import deepdiff
import logging


LOGGER = logging.getLogger(__name__)


def generate_diff_report_lines(
    expected: Any, actual: Any, **kwargs: Any
) -> Optional[List[str]]:
    try:
        custom_operator = (
            compare_helpers_deepdiff_operator.COMPARE_HELPERS_DEEPDIFF_OPERATOR
        )

        diff = deepdiff.DeepDiff(
            expected,
            actual,
            custom_operators=[custom_operator],
            **kwargs,
        )

        return diff.pretty().split("\n")
    except Exception:
        LOGGER.debug("Failed to generate diff report", exc_info=True)
        return None
