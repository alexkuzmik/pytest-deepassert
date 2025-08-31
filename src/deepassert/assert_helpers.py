from typing import List, Any, Optional, Mapping

from . import diff_report


def assert_equal(*, expected: Any, actual: Any):
    """
    expected MUST be left argument so that __eq__ operators
    from our ANY* comparison helpers were called instead of __eq__ operators
    of the actual object
    """
    assert (
        expected == actual
    ), f"Details:\n{diff_report.generate_diff_report(actual=actual, expected=expected)}"


def assert_dicts_equal(
    dict1: Mapping[str, Any],
    dict2: Mapping[str, Any],
    ignore_keys: Optional[List[str]] = None,
) -> None:
    dict1_copy, dict2_copy = {**dict1}, {**dict2}

    ignore_keys = [] if ignore_keys is None else ignore_keys

    for key in ignore_keys:
        dict1_copy.pop(key, None)
        dict2_copy.pop(key, None)

    assert dict1_copy == dict2_copy, f"Details:\n{diff_report.generate_diff_report(
        dict1_copy, dict2_copy
    )}"
