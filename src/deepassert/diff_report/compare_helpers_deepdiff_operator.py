from typing import Any, Tuple
from typing_extensions import override
import deepdiff.operator
import deepdiff.model


class CompareHelpersDeepdiffOperator(deepdiff.operator.BaseOperatorPlus):
    """
    A deepdiff operator for comparing objects via the special comparison helpers.
    It is used to be passed as DeepDiff(custom_operators).
    """

    def __init__(self, helpers_types: Tuple[type, ...]):
        self._helpers_types = helpers_types

    @override
    def match(self, level: deepdiff.model.DiffLevel) -> bool:
        """
        Returns True if either of the items is a special comparison helper type so that
        deepdiff could use `give_up_diffing` method to compare the items instead of the default
        comparison which will fail because of the different types.
        """
        left = level.t1
        right = level.t2
        if isinstance(left, self._helpers_types) or isinstance(
            right, self._helpers_types
        ):
            return True

        return False

    @override
    def give_up_diffing(
        self, level: deepdiff.model.DiffLevel, diff_instance: Any
    ) -> bool:
        """
        If either of the items is a special comparison helper type, it uses the equality operator
        to compare the items instead of the default comparison which will fail because of the different types.
        """
        left = level.t1
        right = level.t2
        if isinstance(left, self._helpers_types):
            return left == right

        return right == left

    @override
    def normalize_value_for_hashing(self, parent: Any, obj: Any) -> Any:
        return obj
