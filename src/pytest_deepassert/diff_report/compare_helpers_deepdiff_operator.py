from typing import Any
from typing_extensions import override
import deepdiff.operator
import deepdiff.model


class CompareHelpersDeepdiffOperator(deepdiff.operator.BaseOperatorPlus):
    """
    A deepdiff operator for comparing objects.

    Designed to support use cases when one of the comparison arguments is a
    special comparison helper type, for example mock.ANY or pytest.approx(...) instance.
    """

    @override
    def match(self, level: deepdiff.model.DiffLevel) -> bool:
        """Always match so that give_up_diffing method is called for comparison"""
        return True

    @override
    def give_up_diffing(
        self, level: deepdiff.model.DiffLevel, diff_instance: Any
    ) -> bool:
        """
        If either of the items is a special comparison helper type, it uses the equality operator.
        Equality operator works as expected only if comparison helper instance is LEFT argument.

        This method checks both ways of equality comparison.
        """

        left = level.t1
        right = level.t2

        return left == right or right == left

    @override
    def normalize_value_for_hashing(self, parent: Any, obj: Any) -> Any:
        return obj


COMPARE_HELPERS_DEEPDIFF_OPERATOR = CompareHelpersDeepdiffOperator()
