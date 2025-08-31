from typing import Any

from . import compare_helpers_deepdiff_operator
from .. import any_compare_helpers
import deepdiff
import logging


SPECIAL_COMPARISON_HELPERS_TYPES = [
    type(any_compare_helpers.ANY_BUT_NONE),
    type(any_compare_helpers.ANY_DICT),
    type(any_compare_helpers.ANY_LIST),
    type(any_compare_helpers.ANY_STRING),
    type(any_compare_helpers.ANY),
]

try:
    import _pytest.python_api
    SPECIAL_COMPARISON_HELPERS_TYPES.append(type(_pytest.python_api.ApproxBase))
except ImportError:
    pass

LOGGER = logging.getLogger(__name__)


def generate_diff_report(expected: Any, actual: Any, **kwargs) -> str:
    try:
        if kwargs.get("custom_operators") is None:
            custom_operators = [
                compare_helpers_deepdiff_operator.CompareHelpersDeepdiffOperator(
                    tuple(SPECIAL_COMPARISON_HELPERS_TYPES)
                )
            ]

        diff = deepdiff.DeepDiff(
            expected,
            actual,
            custom_operators=custom_operators,
            **kwargs,
        )

        return diff.pretty()
    except Exception:
        LOGGER.debug("Failed to generate diff report", exc_info=True)
        return "Failed to generate diff report"
