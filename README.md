# pytest-deepassert

A pytest plugin for enhanced assertion reporting with detailed diffs powered by DeepDiff.

## Why pytest-deepassert?

When testing complex data structures, standard pytest assertions can be really inconvenient as their report messages are based on string comparisons. 

So, if you ever struggled with understanding WHAT EXACTLY is mismatching in your `assert a == b`, `pytest_deepassert` is what you need.

## What is pytest-deepassert?

`pytest_deepassert` is based on `deepdiff` library which can generate very detailed difference reports for various types of objects: int, string, dict, list, tuple, set, frozenset, OrderedDict, NamedTuple and even custom objects!

## Installation

```bash
pip install pytest-deepassert

# Install in development mode
pip install -e ".[dev]"
```

## Key Benefits

### 🎯 **Precise Error Location**
- Pinpoints exact paths where differences occur
- No more hunting through massive data dumps

### 🔍 **Clear Change Description**
- Shows old value → new value for each difference
- Categorizes changes (values changed, items added/removed, etc.)

### 🧩 **Smart Comparison Helpers**
- Works seamlessly with `pytest.approx()`, `mock.ANY`, and any other comparison helpers that you may have implemented already for your project.
- Handles complex nested structures intelligently, even custom objects.

### 📊 **Better Readability**
- Clean, formatted, not cluttered output that's easy to scan

### ⚡ **Zero Configuration**
- Just install and it works
- Can be disabled with `--no-deepassert` flag

## The Problem with Standard Pytest Assertions

### Example 1: Complex Dictionary Comparison

Consider this test with nested dictionaries:

```python
import pytest
from unittest.mock import ANY

def test_user_profile_comparison():
    expected = {
        "user": {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "language": "en"
            },
            "metadata": {
                "created_at": ANY,  # We don't care about exact timestamp
                "last_login": "2023-12-01",
                "login_count": 42,
                "score": pytest.approx(85.5, abs=0.1)  # Approximate float comparison
            }
        },
        "permissions": ["read", "write", "admin"]
    }
    
    actual = {
        "user": {
            "id": 123,
            "name": "Jane Doe",  # Different name
            "email": "jane@example.com",  # Different email
            "preferences": {
                "theme": "light",  # Different theme
                "notifications": True,
                "language": "es"  # Different language
            },
            "metadata": {
                "created_at": "2023-01-01T10:30:00Z",  # This will match ANY
                "last_login": "2023-11-30",  # Different date
                "login_count": 45,  # Different count
                "score": 85.52  # Close enough to match approx
            }
        },
        "permissions": ["read", "write", "admin", "delete"]  # Extra "delete" permission
    }
    
    assert actual == expected
```

**Standard pytest output (with `pytest -vv --no-deepassert`):**
```
example_tests.py::test_user_profile_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_user_profile_comparison _________________________
example_tests.py:47: in test_user_profile_comparison
    assert actual == expected
E   AssertionError: assert {'user': {'id': 123, 'name': 'Jane Doe', 'email': 'jane@example.com', 'preferences': {'theme': 'light', 'notifications': True, 'language': 'es'}, 'metadata': {'created_at': '2023-01-01T10:30:00Z', 'last_login': '2023-11-30', 'login_count': 45, 'score': 85.52}}, 'permissions': ['read', 'write', 'admin', 'delete']} == {'user': {'id': 123, 'name': 'John Doe', 'email': 'john@example.com', 'preferences': {'theme': 'dark', 'notifications': True, 'language': 'en'}, 'metadata': {'created_at': <ANY>, 'last_login': '2023-12-01', 'login_count': 42, 'score': 85.5 ± 0.1}}, 'permissions': ['read', 'write', 'admin']}

E     
E     Differing items:
E     {'permissions': ['read', 'write', 'admin', 'delete']} != {'permissions': ['read', 'write', 'admin']}
E     {'user': {'email': 'jane@example.com', 'id': 123, 'metadata': {'created_at': '2023-01-01T10:30:00Z', 'last_login': '2023-11-30', 'login_count': 45, 'score': 85.52}, 'name': 'Jane Doe', ...}} != {'user': {'email': 'john@example.com', 'id': 123, 'metadata': {'created_at': <ANY>, 'last_login': '2023-12-01', 'login_count': 42, 'score': 85.5 ± 0.1}, 'name': 'John Doe', ...}}

E     
E     Full diff:
E       {
E           'permissions': [
E               'read',
E               'write',
E               'admin',
E     +         'delete',
E           ],
E           'user': {
E     -         'email': 'john@example.com',
E     ?                    ^^
E     +         'email': 'jane@example.com',
E     ?                    ^ +
E               'id': 123,
E               'metadata': {
E     -             'created_at': <ANY>,
E     +             'created_at': '2023-01-01T10:30:00Z',
E     -             'last_login': '2023-12-01',
E     ?                                  ^  -
E     +             'last_login': '2023-11-30',
E     ?                                  ^ +
E     -             'login_count': 42,
E     ?                             ^
E     +             'login_count': 45,
E     ?                             ^
E     -             'score': 85.5 ± 0.1,
E     ?                          ^^^^^^
E     +             'score': 85.52,
E     ?                          ^
E               },
E     -         'name': 'John Doe',
E     ?                   ^^
E     +         'name': 'Jane Doe',
E     ?                   ^ +
E               'preferences': {
E     -             'language': 'en',
E     ?                           ^
E     +             'language': 'es',
E     ?                           ^
E                   'notifications': True,
E     -             'theme': 'dark',
E     ?                       ^^^^
E     +             'theme': 'light',
E     ?                       ^^^^^
E               },
E           },
E       }
```

**With pytest-deepassert (with `pytest -vv`):**
```
example_tests.py::test_user_profile_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_user_profile_comparison _________________________
example_tests.py:47: in test_user_profile_comparison
    assert actual == expected
E   assert 
E     DeepAssert detailed comparison:
E         Item root['permissions'][3] added to iterable.
E         Value of root['user']['name'] changed from "John Doe" to "Jane Doe".
E         Value of root['user']['email'] changed from "john@example.com" to "jane@example.com".
E         Value of root['user']['preferences']['theme'] changed from "dark" to "light".
E         Value of root['user']['preferences']['language'] changed from "en" to "es".
E         Value of root['user']['metadata']['last_login'] changed from "2023-12-01" to "2023-11-30".
E         Value of root['user']['metadata']['login_count'] changed from 42 to 45.
E     
E     [... standard pytest diff continues below ...]
```

**Notice how `pytest-deepassert`:**
- ✅ **Ignores `created_at`** - because it matches `ANY`
- ✅ **Ignores `score`** - because `85.52` is within `pytest.approx(85.5, abs=0.1)`
- 🎯 **Only shows actual differences** - name, email, theme, language, last_login, login_count, and added delete permission

### Example 2: List of Objects with Special Comparisons

```python
def test_api_response_comparison():
    expected = [
        {"id": 1, "name": "Product A", "price": pytest.approx(19.99, rel=0.01), "in_stock": True},
        {"id": 2, "name": "Product B", "price": 29.99, "in_stock": False, "created_at": ANY},
        {"id": 3, "name": "Product C", "price": 39.99, "in_stock": True}
    ]
    
    actual = [
        {"id": 1, "name": "Product A", "price": 19.98, "in_stock": True},  # Close price (matches approx)
        {"id": 2, "name": "Product B", "price": 24.99, "in_stock": True, "created_at": "2023-12-01"},  # Price and stock changed, but created_at matches ANY
        {"id": 4, "name": "Product D", "price": 49.99, "in_stock": False}  # Different product
    ]
    
    assert actual == expected
```

**Standard pytest output (with `pytest -vv --no-deepassert`):**
```
example_tests.py::test_api_response_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_api_response_comparison _________________________
example_tests.py:64: in test_api_response_comparison
    assert actual == expected
E   AssertionError: assert [{'id': 1, 'name': 'Product A', 'price': 19.98, 'in_stock': True}, {'id': 2, 'name': 'Product B', 'price': 24.99, 'in_stock': True, 'created_at': '2023-12-01'}, {'id': 4, 'name': 'Product D', 'price': 49.99, 'in_stock': False}] == [{'id': 1, 'name': 'Product A', 'price': 19.99 ± 0.1999, 'in_stock': True}, {'id': 2, 'name': 'Product B', 'price': 29.99, 'in_stock': False, 'created_at': <ANY>}, {'id': 3, 'name': 'Product C', 'price': 39.99, 'in_stock': True}]

E     
E     At index 1 diff: {'id': 2, 'name': 'Product B', 'price': 24.99, 'in_stock': True, 'created_at': '2023-12-01'} != {'id': 2, 'name': 'Product B', 'price': 29.99, 'in_stock': False, 'created_at': <ANY>}

E     
E     Full diff:
E       [
E           {
E               'id': 1,
E               'in_stock': True,
E               'name': 'Product A',
E     -         'price': 19.99 ± 0.1999,
E     ?                      ^^^^^^^^^^
E     +         'price': 19.98,
E     ?                      ^
E           },
E           {
E     -         'created_at': <ANY>,
E     +         'created_at': '2023-12-01',
E               'id': 2,
E     -         'in_stock': False,
E     ?                     ^^^^
E     +         'in_stock': True,
E     ?                     ^^^
E               'name': 'Product B',
E     -         'price': 29.99,
E     ?                   ^
E     +         'price': 24.99,
E     ?                   ^
E           },
E           {
E     -         'id': 3,
E     ?               ^
E     +         'id': 4,
E     ?               ^
E     -         'in_stock': True,
E     ?                     ^^^
E     +         'in_stock': False,
E     ?                     ^^^^
E     -         'name': 'Product C',
E     ?                          ^
E     +         'name': 'Product D',
E     ?                          ^
E     -         'price': 39.99,
E     ?                  ^
E     +         'price': 49.99,
E     ?                  ^
E           },
E       ]
```

**With `pytest-deepassert`:**
```
example_tests.py::test_api_response_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_api_response_comparison _________________________
example_tests.py:64: in test_api_response_comparison
    assert actual == expected
E   assert 
E     DeepAssert detailed comparison:
E         Value of root[1]['price'] changed from 29.99 to 24.99.
E         Value of root[1]['in_stock'] changed from False to True.
E         Value of root[2]['id'] changed from 3 to 4.
E         Value of root[2]['name'] changed from "Product C" to "Product D".
E         Value of root[2]['price'] changed from 39.99 to 49.99.
E         Value of root[2]['in_stock'] changed from True to False.
E     
E     [... standard pytest diff continues below ...]
```

**Notice how `pytest-deepassert`:**
- ✅ **Ignores `root[0]['price']`** - because `19.98` is within `pytest.approx(19.99, rel=0.01)`
- ✅ **Ignores `root[1]['created_at']`** - because `"2023-12-01"` matches `ANY`
- 🎯 **Only shows actual differences** - price and stock changes for Product B, and all changes for the third item

### Example 3: Working with pytest.approx and mock.ANY

`pytest-deepassert` seamlessly handles special comparison helpers:

```python
import pytest
from unittest.mock import ANY

def test_with_special_comparisons():
    expected = {
        "timestamp": ANY,  # We don't care about exact timestamp
        "value": pytest.approx(3.14159, abs=0.001),  # Approximate float comparison
        "metadata": {
            "version": "1.0.0",
            "debug": False
        }
    }
    
    actual = {
        "timestamp": "2023-12-01T10:30:00Z",
        "value": 3.14160,  # Close enough
        "metadata": {
            "version": "1.0.1",  # Different version
            "debug": False
        }
    }
    
    assert actual == expected
```

**With `pytest-deepassert`:**
```
>       assert actual == expected
E   assert 
E     DeepAssert detailed comparison:
E         Value of root['metadata']['version'] changed from "1.0.0" to "1.0.1".
E     
E     [... standard pytest diff continues below ...]
```


## Usage

Once installed, `pytest-deepassert` *automatically* enhances all your `==` assertions. No code changes required!

```python
def test_my_data():
    expected = {"a": 1, "b": {"c": 2, "d": 3}}
    actual = {"a": 1, "b": {"c": 4, "d": 3}}
    
    assert actual == expected  # Enhanced output automatically!
```

### Disabling for Specific Tests

If you need to disable enhanced assertions for specific cases:

```bash
pytest --no-deepassert
```