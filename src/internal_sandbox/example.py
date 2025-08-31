from deepassert import assert_dicts_equal
from deepassert.any_compare_helpers import ANY_BUT_NONE, ANY_DICT

d1 = {
    "a": 1,
    "b": 2,
    "c": None,
    "d": "d-value1",
    "e": "e-value1",
}

d2 = {
    "a": 1,
    "b": ANY_BUT_NONE,
    "c": ANY_DICT,
    "d": "d-value2",
    "e": "e-value2",
}

assert_dicts_equal(d1, d2)
