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

## 📋 Table of Contents

- [🎯 Why pytest-deepassert?](#-why-pytest-deepassert)
- [✨ What is pytest-deepassert?](#-what-is-pytest-deepassert)
- [🚀 Installation](#-installation)
- [🌟 Key Features](#-key-features)
- [❌ The Problem with Standard Assertions](#-the-problem-with-standard-assertions)
- [💡 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [🔧 API Reference](#-api-reference)
- [⚠️ Limitations](#️-limitations)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Why pytest-deepassert?

When testing complex data structures, standard pytest assertions can be **frustrating** and **time-consuming**:

- 🔍 **Hard to spot differences** in large nested objects
- 📊 **Cluttered output** that's difficult to parse
- 🕵️ **Manual hunting** through string comparisons
- 🤯 **Overwhelming diffs** for simple changes

If you've ever struggled with understanding **WHAT EXACTLY** is mismatching in your `assert a == b`, `pytest-deepassert` is what you need!

## ✨ What is pytest-deepassert?

`pytest-deepassert` is a powerful pytest plugin built on the robust [`deepdiff`](https://github.com/seperman/deepdiff) library. It provides **crystal-clear, detailed difference reports** for various data types:

- 📦 **Basic types**: `int`, `string`, `float`, `bool`
- 📚 **Collections**: `dict`, `list`, `tuple`, `set`, `frozenset`
- 🏗️ **Advanced types**: `OrderedDict`, `NamedTuple`, custom objects
- 🔧 **Smart helpers**: Works with `pytest.approx()`, `mock.ANY`, and custom comparators

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

## 🌟 Key Features

<table>
<tr>
<td width="50%">

### 🎯 **Precise Error Location**
- 📍 Pinpoints **exact paths** where differences occur
- 🚫 No more hunting through massive data dumps
- 🔍 Shows **specific field names** and **array indices**

### 🔄 **Clear Change Description**
- ➡️ Shows `left value` → `right value` for each difference
- 📂 Categorizes changes (values changed, items added/removed)
- 🏷️ **Human-readable** change descriptions

</td>
<td width="50%">

### 🧩 **Smart Comparison Helpers**
- ✅ Works seamlessly with `pytest.approx()`, `mock.ANY`
- 🔧 Supports **custom comparison helpers**
- 🏗️ Handles complex nested structures intelligently

### ⚡ **Zero Configuration**
- 🚀 **Just install and it works** - no setup required
- 🎛️ Can be disabled with `--no-deepassert` flag
- 🔧 **Drop-in replacement** for standard assertions

</td>
</tr>
</table>

### 📊 **Enhanced Readability**

| Standard pytest | pytest-deepassert |
|---|---|
| 😵 Overwhelming string diffs | ✨ Clean, categorized changes |
| 🔍 Manual hunting for differences | 🎯 Precise error locations |
| 📄 Cluttered output | 📋 Organized, scannable format |

---

## ❌ The Problem with Standard Assertions

> **TL;DR**: Standard pytest assertions become **unreadable** and **time-consuming** with complex data structures.

### 📋 Example 1: Complex Dictionary Comparison

Consider this realistic test with nested dictionaries:

<details>
<summary><strong>🔍 Click to see the test code</strong></summary>

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

#### 😵 **Standard pytest output** (with `pytest -vv --no-deepassert`)

<details>
<summary><strong>❌ Click to see the messy output</strong></summary>

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
| **Smart filtering** | Shows `created_at` and `score` differences | ✅ **Ignores `created_at`** (matches `ANY`) |
| **Precision** | Highlights irrelevant changes | ✅ **Ignores `score`** (within `pytest.approx` tolerance) |
| **Clarity** | Overwhelming wall of text | 🎯 **Only shows actual differences** |
| **Readability** | Hard to scan | 📋 **Clean, organized output** |


### 📋 Example 2: Smart Comparison Helpers

`pytest-deepassert` seamlessly handles special comparison helpers:

<details>
<summary><strong>🔍 Click to see the test code</strong></summary>

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

#### ✨ **With pytest-deepassert**

```diff
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

### 🚀 **Automatic Enhancement**

Once installed, `pytest-deepassert` **automatically** enhances all your `==` assertions. No code changes required!

```python
def test_my_data():
    expected = {"a": 1, "b": {"c": 2, "d": 3}}
    actual = {"a": 1, "b": {"c": 4, "d": 3}}

    assert actual == expected  # ✨ Enhanced output automatically!
```

### 🎛️ **Configuration Options**

#### Disable for specific test runs

```bash
pytest --no-deepassert
```

#### Disable for specific tests

```python
import pytest

@pytest.mark.no_deepassert
def test_without_enhancement():
    # This test will use standard pytest assertions
    assert actual == expected
```

---

## ⚙️ Configuration

`pytest-deepassert` works out of the box with **zero configuration**. However, you can customize its behavior:

### Command Line Options

| Option | Description |
|--------|-------------|
| `--no-deepassert` | Disable pytest-deepassert for this test run |
| `--deepassert-verbose` | Show additional debugging information |

### pytest.ini Configuration

```ini
[tool:pytest]
addopts = --no-deepassert  # Disable by default
```

---

## 🔧 API Reference

### `pytest_deepassert.equal(left, right)`

For assertions outside test functions:

```python
from pytest_deepassert import equal

def validate_data(actual, expected):
    equal(actual, expected)  # Enhanced diff on failure
```

**Parameters:**
- `left`: The actual value
- `right`: The expected value

**Raises:**
- `AssertionError`: With detailed diff report if values don't match

---

## ⚠️ Limitations

- **Scope**: Only enhances assertions in test functions (pytest limitation)
- **Workaround**: Use `pytest_deepassert.equal()` for assertions outside tests
- **Performance**: Minimal overhead for passing tests, slight overhead for failing tests

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/alexkuzmik/pytest-deepassert.git
cd pytest-deepassert

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pytest_deepassert

# Run specific test file
pytest tests/unit/test_equal.py
```

### 📝 Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Submit a pull request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **📦 [PyPI Package](https://pypi.org/project/pytest-deepassert/)**
- **🐙 [GitHub Repository](https://github.com/alexkuzmik/pytest-deepassert)**
- **🐛 [Issue Tracker](https://github.com/alexkuzmik/pytest-deepassert/issues)**
- **📚 [DeepDiff Library](https://github.com/seperman/deepdiff)**

---

<div align="center">

**Made with ❤️ by [Alexander Kuzmik](https://github.com/alexkuzmik)**

*If this project helped you, please consider giving it a ⭐ on GitHub!*

</div>
