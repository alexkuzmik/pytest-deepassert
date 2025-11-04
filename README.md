<div align="center">

# 🔍 pytest-deepassert

</div>
<div align="center">

[![PyPI version](https://badge.fury.io/py/pytest-deepassert.svg)](https://pypi.org/project/pytest-deepassert/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-deepassert.svg)](https://pypi.org/project/pytest-deepassert/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/pytest-deepassert)](https://pepy.tech/project/pytest-deepassert)

**Enhanced pytest assertions with detailed diffs powered by DeepDiff**

*Stop hunting through massive data dumps. Get precise, readable assertion failures.*

</div>

---

## Table of Contents

- [What is it for?](#what-is-it-for)
- [How it works](#how-it-works)
- [Installation](#installation)
- [Key Features](#key-features)
- [Comparison with Standard Assertions](#comparison-with-standard-assertions)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Limitations](#limitations)
- [License](#license)

---

## What is it for?

When testing that one complex data structure equals another, you may have situations when only some small details differ, but it is really hard to see which ones because of the cluttered comparison report. That's when `pytest-deepassert` helps:

- **Quicker identification** of differences in large & nested objects
- **Focused output** that highlights what matters
- **Direct navigation** to specific changes
- **Structured diffs** for complex data

If you've ever struggled with understanding **WHAT EXACTLY** is mismatching in your `assert a == b` statement, `pytest-deepassert` is what you need!

## How it works

`pytest-deepassert` is a pytest plugin built on powerful [`deepdiff`](https://github.com/seperman/deepdiff) library. It provides **clear, detailed difference reports** for various data types:

- **Basic types**: `int`, `string`, `float`, `bool`
- **Collections**: `dict`, `list`, `tuple`, `set`, `frozenset`
- **Advanced types**: `OrderedDict`, `NamedTuple`, custom objects

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install pytest-deepassert
```

### From Source

```bash
git clone https://github.com/alexkuzmik/pytest-deepassert.git
cd pytest-deepassert
pip install -e .
```

**Requirements**: Python 3.8+ and pytest 6.0+

## ✨ Key Features

### **Precise Error Location**
- Pinpoints **exact paths** where differences occur
- No more hunting through massive data dumps
- Shows **specific field names**, **values**, and **array indices**

### **Clear Change Description**
- Shows `left value` → `right value` for each difference
- Categorizes changes (values changed, items added/removed)
- **Human-readable** change descriptions

### **Smart Comparison Helpers**
- Works seamlessly with `pytest.approx()`, `mock.ANY` and any custom comparator utilities
- Handles complex nested structures intelligently

### **Simple Opt-In**
- **Enable with `--deepassert` flag** - disabled by default to avoid interference
- No additional configuration needed
- **Drop-in replacement** for standard assertions when enabled

---

## 📊 Comparison with Standard Assertions

> **TL;DR**: Standard pytest assertions work great for simple cases, but their string comparison reports are not optimized for complex data structures and utility comparator objects. That's where `pytest-deepassert` shines.

### Example 1: Complex Dictionary Comparison

Consider this realistic test with nested dictionaries:

<details>
<summary><strong>Click to see the test code</strong></summary>

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

    assert expected == actual
```

</details>

#### 📄 **Standard pytest output**

<details>
<summary><strong>Click to see the standard output</strong></summary>

```
example_test1.py::test_user_profile_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_user_profile_comparison _________________________
example_test1.py:45: in test_user_profile_comparison
    assert expected == actual
E   AssertionError: assert {'user': {'id': 123, 'name': 'John Doe', 'email': 'john@example.com', 'preferences': {'theme': 'dark', 'notifications': True, 'language': 'en'}, 'metadata': {'created_at': <ANY>, 'last_login': '2023-12-01', 'login_count': 42, 'score': 85.5 ± 0.1}}, 'permissions': ['read', 'write', 'admin']} == {'user': {'id': 123, 'name': 'Jane Doe', 'email': 'jane@example.com', 'preferences': {'theme': 'light', 'notifications': True, 'language': 'es'}, 'metadata': {'created_at': '2023-01-01T10:30:00Z', 'last_login': '2023-11-30', 'login_count': 45, 'score': 85.52}}, 'permissions': ['read', 'write', 'admin', 'delete']}

E
E     Differing items:
E     {'permissions': ['read', 'write', 'admin']} != {'permissions': ['read', 'write', 'admin', 'delete']}
E     {'user': {'email': 'john@example.com', 'id': 123, 'metadata': {'created_at': <ANY>, 'last_login': '2023-12-01', 'login_count': 42, 'score': 85.5 ± 0.1}, 'name': 'John Doe', ...}} != {'user': {'email': 'jane@example.com', 'id': 123, 'metadata': {'created_at': '2023-01-01T10:30:00Z', 'last_login': '2023-11-30', 'login_count': 45, 'score': 85.52}, 'name': 'Jane Doe', ...}}

E
E     Full diff:
E       {
E           'permissions': [
E               'read',
E               'write',
E               'admin',
E     -         'delete',
E           ],
E           'user': {
E     -         'email': 'jane@example.com',
E     ?                    ^ -
E     +         'email': 'john@example.com',
E     ?                    ^^
E               'id': 123,
E               'metadata': {
E     -             'created_at': '2023-01-01T10:30:00Z',
E     +             'created_at': <ANY>,
E     -             'last_login': '2023-11-30',
E     ?                                   ---
E     +             'last_login': '2023-12-01',
E     ?                                  +++
E     -             'login_count': 45,
E     ?                             ^
E     +             'login_count': 42,
E     ?                             ^
E     -             'score': 85.52,
E     ?                          ^
E     +             'score': 85.5 ± 0.1,
E     ?                          ^^^^^^
E               },
E     -         'name': 'Jane Doe',
E     ?                   ^ -
E     +         'name': 'John Doe',
E     ?                   ^^
E               'preferences': {
E     -             'language': 'es',
E     ?                           ^
E     +             'language': 'en',
E     ?                           ^
E                   'notifications': True,
E     -             'theme': 'light',
E     ?                       ^^^^^
E     +             'theme': 'dark',
E     ?                       ^^^^
E               },
E           },
E       }
```

</details>

#### ✨ **With pytest-deepassert** (with `pytest --deepassert -vv`)

```
example_test1.py::test_user_profile_comparison FAILED

======================================== FAILURES ========================================
_________________________ test_user_profile_comparison _________________________
example_test1.py:45: in test_user_profile_comparison
    assert expected == actual
E   assert
E     DeepAssert detailed comparison:
E         Item root['permissions'][3] ("delete") added to iterable.
E         Value of root['user']['name'] changed from "John Doe" to "Jane Doe".
E         Value of root['user']['email'] changed from "john@example.com" to "jane@example.com".
E         Value of root['user']['preferences']['theme'] changed from "dark" to "light".
E         Value of root['user']['preferences']['language'] changed from "en" to "es".
E         Value of root['user']['metadata']['last_login'] changed from "2023-12-01" to "2023-11-30".
E         Value of root['user']['metadata']['login_count'] changed from 42 to 45.
E
E     [... standard pytest diff continues below ...]
```

### 🎯 **Key Improvements**

| Feature | Standard pytest | pytest-deepassert |
|---------|----------------|-------------------|
| **Smart filtering** | Shows all field comparisons | ✅ **Ignores `created_at`** (matches `ANY`) |
| **Precision** | Comprehensive diff coverage | ✅ **Ignores `score`** (within `pytest.approx` tolerance) |
| **Focus** | Complete context provided | 🎯 **Highlights actual differences** |
| **Format** | String-based comparison | 📋 **Structured, categorized output** |


### 📋 Example 2: Smart Comparison Helpers

`pytest-deepassert` seamlessly handles special comparison helpers:

<details>
<summary><strong>Click to see the test code</strong></summary>

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

    assert expected == actual
```

</details>

#### 📄 **Standard pytest output**

<details>
<summary><strong>Click to see the standard output</strong></summary>

```
example_test2.py::test_with_special_comparisons FAILED

======================================== FAILURES ========================================
______________________________________ test_with_special_comparisons _______________________________________
example_test2.py:23: in test_with_special_comparisons
    assert expected == actual
E   AssertionError: assert {'timestamp': <ANY>, 'value': 3.14159 ± 0.001, 'metadata': {'version': '1.0.0', 'debug': False}} == {'timestamp': '2023-12-01T10:30:00Z', 'value': 3.1416, 'metadata': {'version': '1.0.1', 'debug': False}}

E
E     Common items:
E     {'timestamp': <ANY>, 'value': 3.14159 ± 0.001}
E     Differing items:
E     {'metadata': {'debug': False, 'version': '1.0.0'}} != {'metadata': {'debug': False, 'version': '1.0.1'}}

E
E     Full diff:
E       {
E           'metadata': {
E               'debug': False,
E     -         'version': '1.0.1',
E     ?                         ^
E     +         'version': '1.0.0',
E     ?                         ^
E           },
E     -     'timestamp': '2023-12-01T10:30:00Z',
E     +     'timestamp': <ANY>,
E     -     'value': 3.1416,
E     ?                   ^
E     +     'value': 3.14159 ± 0.001,
E     ?                   ^^^^^^^^^^
E       }
```

</details>

#### ✨ **With pytest-deepassert**

```
example_test2.py::test_with_special_comparisons FAILED

======================================== FAILURES ========================================
______________________________________ test_with_special_comparisons _______________________________________
example_test2.py:23: in test_with_special_comparisons
    assert expected == actual
E   assert
E     DeepAssert detailed comparison:
E         Value of root['metadata']['version'] changed from "1.0.0" to "1.0.1".
E
E     [... standard pytest diff continues below ...]
```

**Notice**: Only the **actual difference** (`version`) is shown. The `timestamp` and `value` fields are correctly ignored!

---

## 💡 Usage

After installation, enable `pytest-deepassert` by passing the `--deepassert` flag when running pytest:

```bash
pytest --deepassert
```

This will enhance all your `==` assertions inside the tests. No code changes required!

---

## Configuration

`pytest-deepassert` is **disabled by default** to avoid any interference with your existing test suite. Enable it when needed:

### Command Line Options

| Option | Description |
|--------|-------------|
| `--deepassert` | Enable pytest-deepassert for this test run |


---


## API Reference

### `pytest_deepassert.equal(left, right, verbose_level=2)`

For use cases where you need enhanced assertions outside of test modules (e.g., in helper functions), you can use the `equal()` function directly.

**Parameters:**
- `left` (Any): The expected object
- `right` (Any): The actual object
- `verbose_level` (int, optional): Controls the verbosity of the diff report. Default: `2`
  - `0`: Minimal output (only reports if objects are different)
  - `1`: Standard output (shows changes with brief details)
  - `2`: Detailed output (shows full changes with all details and types)

**Example:**

```python
import pytest_deepassert

def helper_function_for_assertion(actual, expected):
    # Use default verbose_level=2 for detailed output
    pytest_deepassert.equal(expected, actual)

def another_helper(actual, expected):
    # Use verbose_level=1 for less detailed output
    pytest_deepassert.equal(expected, actual, verbose_level=1)
```

**Note:** The traceback will automatically hide the internal frames of the `equal()` function, showing only where it was called from.

---

## Limitations

The tool only enhances assertions inside the test modules (pytest limitation).
If you want to have deep assertion reports in the other modules of your project (e.g. some helper functions for your testlib), consider using `pytest_deepassert.equal(left, right)` function as described in the [API Reference](#api-reference) section.


---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Links

- **[PyPI Package](https://pypi.org/project/pytest-deepassert/)**
- **[GitHub Repository](https://github.com/alexkuzmik/pytest-deepassert)**
- **[Issue Tracker](https://github.com/alexkuzmik/pytest-deepassert/issues)**
- **[DeepDiff Library](https://github.com/seperman/deepdiff)**

---

<div align="center">

**Made by [Alexander Kuzmik](https://github.com/alexkuzmik)**

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>
