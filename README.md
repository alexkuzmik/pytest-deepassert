# 🔍 pytest-deepassert

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

- [Why pytest-deepassert?](#why-pytest-deepassert)
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

## Why pytest-deepassert?

When testing complex data structures equality, you may have situations when only some small details differ, but it is really hard to see which ones because of the cluttered comparison report:

- **Quicker identification** of differences in large & nested objects
- **Focused output** that highlights what matters
- **Direct navigation** to specific changes
- **Structured diffs** for complex data

If you've ever struggled with understanding **WHAT EXACTLY** is mismatching in your `assert a == b` statement, `pytest-deepassert` is what you need!

## How it works

`pytest-deepassert` is a powerful pytest plugin built on [`deepdiff`](https://github.com/seperman/deepdiff) library. It provides **clear, detailed difference reports** for various data types:

- **Basic types**: `int`, `string`, `float`, `bool`
- **Collections**: `dict`, `list`, `tuple`, `set`, `frozenset`
- **Advanced types**: `OrderedDict`, `NamedTuple`, custom objects
- **Smart helpers**: Works with `pytest.approx()`, `mock.ANY`, and your custom comparators

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
- Shows **specific field names** and **array indices**

### **Clear Change Description**
- Shows `left value` → `right value` for each difference
- Categorizes changes (values changed, items added/removed)
- **Human-readable** change descriptions

### **Smart Comparison Helpers**
- Works seamlessly with `pytest.approx()`, `mock.ANY`
- Supports **custom comparison helpers**
- Handles complex nested structures intelligently

### **Zero Configuration**
- **Just install and it works** - no setup required
- Can be disabled with `--no-deepassert` flag
- **Drop-in replacement** for standard assertions

---

## 📊 Comparison with Standard Assertions

> **TL;DR**: Standard pytest assertions work great for simple cases, but `pytest-deepassert` provides enhanced clarity for complex data structures.

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

    assert actual == expected
```

</details>

#### 📄 **Standard pytest output**

<details>
<summary><strong>Click to see the standard output</strong></summary>

```diff
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

</details>

#### ✨ **With pytest-deepassert** (with `pytest -vv`)

```diff
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

    assert actual == expected
```

</details>

#### 📄 **Standard pytest output**

<details>
<summary><strong>Click to see the standard output</strong></summary>

```
>       assert actual == expected
E       AssertionError: assert {'timestamp': '2023-12-01T10:30:00Z', 'value': 3.1416, 'metadata': {'version': '1.0.1', 'debug': False}} == {'timestamp': <ANY>, 'value': 3.14159 ± 0.001, 'metadata': {'version': '1.0.0', 'debug': False}}
E
E       Differing items:
E       {'metadata': {'version': '1.0.1', 'debug': False}} != {'metadata': {'version': '1.0.0', 'debug': False}}
E       {'timestamp': '2023-12-01T10:30:00Z'} != {'timestamp': <ANY>}
E       {'value': 3.1416} != {'value': 3.14159 ± 0.001}
E
E       Full diff:
E         {
E       -     'metadata': {'debug': False, 'version': '1.0.0'},
E       ?                                           ^
E       +     'metadata': {'debug': False, 'version': '1.0.1'},
E       ?                                           ^
E       -     'timestamp': <ANY>,
E       +     'timestamp': '2023-12-01T10:30:00Z',
E       -     'value': 3.14159 ± 0.001,
E       ?                    ^^^^^^^^
E       +     'value': 3.1416,
E       ?                   ^
E         }
```

</details>

#### ✨ **With pytest-deepassert**

```
>       assert actual == expected
E   assert
E     DeepAssert detailed comparison:
E         Value of root['metadata']['version'] changed from "1.0.0" to "1.0.1".
E
E     [... standard pytest diff continues below ...]
```

**Notice**: Only the **actual difference** (`version`) is shown. The `timestamp` and `value` fields are correctly ignored!

---

## 💡 Usage

### **Automatic Enhancement**

Once installed, `pytest-deepassert` **automatically** enhances all your `==` assertions inside the tests. No code changes required!


### **Configuration Options**

#### Disable deepassert

```bash
pytest --no-deepassert
```

---

## Configuration

`pytest-deepassert` works out of the box with **zero configuration**. However, you can customize its behavior:

### Command Line Options

| Option | Description |
|--------|-------------|
| `--no-deepassert` | Disable pytest-deepassert for this test run |

### pytest.ini Configuration

```ini
[tool:pytest]
addopts = --no-deepassert  # Disable by default
```

---


## Limitations

Only enhances assertions in test functions (pytest limitation).
If you want to have deep assertion reports in other places, consider using `pytest_deepassert.equal(left, right)` function.

```python
import pytest_deepassert

def helper_function_for_assertion(actual, expected):
    pytest_deepassert.equal(actual, expected)  # Enhanced diff on failure
```


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

*This plugin comes from my desire to share a tool that I initially built for myself and my team while working on [Opik](https://github.com/comet-ml/opik) python library.
It's built above another amazing open-sourced project - [deepdiff](https://github.com/seperman/deepdiff), so I guess I owe to the community a bit :).*

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>
