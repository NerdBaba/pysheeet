---
title: Pytest
---

# Pytest

Source  
[src/basic/pytest\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/pytest_.py)

[[toc]]

pytest is the de facto standard testing framework for Python. It requires minimal boilerplate — write plain functions with `assert` statements and pytest handles test discovery, detailed failure reporting, fixtures, parameterization, and plugin integration. Install with `pip install pytest`. The framework automatically discovers test files matching `test_*.py` or `*_test.py` patterns.

## Basic Test Functions

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic test functions](https://realpython.com/search?q=basic+test+functions).
:::

Write test functions prefixed with `test_`. Use plain `assert` — pytest rewrites assertions to provide detailed failure context.

```python
# test_basic.py
def test_addition():
    assert 1 + 1 == 2


def test_string():
    result = "hello world"
    assert "hello" in result
    assert result.upper() == "HELLO WORLD"


def test_collection():
    items = [1, 2, 3]
    assert len(items) == 3
    assert 2 in items
```

Run with: `pytest test_basic.py` or `pytest -v` for verbose.

## Assertion Introspection

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pytest assertion introspection](https://realpython.com/search?q=pytest+assertion+introspection).
:::

When an assertion fails, pytest displays the actual values — no need for custom error messages.

```python
def test_failure():
    expected = {"name": "Alice", "age": 30}
    actual = {"name": "Alice", "age": 31}
    assert actual == expected
    # Detailed diff: E       -  'age': 30
    #                        ?          ^
    #                        E       +  'age': 31
    #                        ?          ^
```

## Fixtures

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on fixtures](https://realpython.com/search?q=fixtures).
:::

Fixtures provide reusable test setup and teardown. They use dependency injection — just declare the fixture name as a parameter.

```python
import pytest


@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"name": "Alice", "scores": [90, 85, 92]}


@pytest.fixture
def db_connection():
    """Set up and tear down a database connection."""
    conn = create_connection("test.db")
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def config():
    """Load once per session, not per test."""
    return load_config("test_config.yaml")


def test_scores(sample_data):
    assert sum(sample_data["scores"]) == 267


def test_db(db_connection):
    assert db_connection.is_connected()
```

Fixture scopes: `function` (default, per test), `class`, `module`, `session` (once per run).

## conftest.py — Shared Fixtures

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on conftest py shared fixtures](https://realpython.com/search?q=conftest+py+shared+fixtures).
:::

Place shared fixtures in `conftest.py` to make them available across multiple test files without importing.

```python
# conftest.py
import pytest


@pytest.fixture
def sample_data():
    return {"name": "Alice", "scores": [90, 85, 92]}


@pytest.fixture
def temp_dir(tmp_path):
    """Provide a temporary directory for file tests."""
    d = tmp_path / "test_data"
    d.mkdir()
    return d
```

```python
# test_user.py — uses fixtures from conftest.py
def test_user_name(sample_data):
    assert sample_data["name"] == "Alice"


def test_temp_file(temp_dir):
    f = temp_dir / "test.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"
```

## Built-in Fixtures

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on built-in fixtures](https://realpython.com/search?q=built-in+fixtures).
:::

Pytest includes several built-in fixtures for common needs.

```python
# tmp_path — temporary directory (Path object)
def test_tmpdir(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "hello.txt"
    f.write_text("content")
    assert f.read_text() == "content"


# monkeypatch — modify attributes, env vars, etc.
def test_monkeypatch(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    assert os.environ["DATABASE_URL"] == "sqlite:///test.db"


def test_monkeypatch_dict(monkeypatch):
    config = {"host": "localhost"}
    monkeypatch.setitem(config, "host", "127.0.0.1")
    assert config["host"] == "127.0.0.1"


def test_monkeypatch_attr(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda x: True)
    assert os.path.exists("/nonexistent")  # Returns True
```

## Parametrize

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on parametrize](https://realpython.com/search?q=parametrize).
:::

Run a test function with multiple input values, generating separate test cases for each combination.

```python
import pytest


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert a + b == expected


# Cartesian product of parameters
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [-1, 1])
def test_multiply(x, y):
    assert x * y in {0, 1, -1}


# Parametrize with custom IDs
@pytest.mark.parametrize("text,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
], ids=["lowercase", "lowercase2", "empty"])
def test_uppercase(text, expected):
    assert text.upper() == expected
```

## Skip and Xfail

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on skip and xfail](https://realpython.com/search?q=skip+and+xfail).
:::

Skip tests conditionally or mark expected failures.

```python
import pytest
import sys


# Skip unconditionally
@pytest.mark.skip(reason="Not implemented yet")
def test_feature():
    pass


# Skip conditionally
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_feature():
    pass


# Skip if module not available
@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux only")
def test_linux_specific():
    pass


# Expected failure — test that is known to fail
@pytest.mark.xfail(reason="Known bug #123", strict=False)
def test_known_bug():
    assert 1 == 2  # Expected to fail, won't break CI


# Xfail with condition
@pytest.mark.xfail(sys.platform == "win32", reason="Fails on Windows")
def test_windows_bug():
    pass


# Force run even if marked xfail
@pytest.mark.xfail(strict=True, run=True)
def test_strict_xfail():
    assert 1 == 1  # Will fail if this passes unexpectedly
```

## approx — Floating Point Comparison

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pytest approx floating point](https://realpython.com/search?q=pytest+approx+floating+point).
:::

Compare floating-point numbers with tolerance. Avoids flaky tests from precision artifacts.

```python
import pytest


def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_approx_with_tolerance():
    assert (0.1 + 0.2) == pytest.approx(0.3, rel=1e-6)   # Relative tolerance
    assert (0.1 + 0.2) == pytest.approx(0.3, abs=1e-6)   # Absolute tolerance


def test_approx_arrays():
    assert [0.1 + 0.2, 0.2 + 0.3] == pytest.approx([0.3, 0.5])


def test_approx_dict():
    assert {"a": 0.1 + 0.2} == pytest.approx({"a": 0.3})


def test_approx_numpy():
    import numpy as np
    assert np.array([0.1 + 0.2]) == pytest.approx(np.array([0.3]))
```

## raises — Exception Testing

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pytest raises exception](https://realpython.com/search?q=pytest+raises+exception).
:::

Verify that code raises expected exceptions with specific messages.

```python
import pytest


def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_raises_with_message():
    with pytest.raises(ValueError, match="invalid value"):
        int("not_a_number")


def test_raises_inspect():
    with pytest.raises(KeyError) as exc_info:
        d = {}
        _ = d["missing"]

    assert "missing" in str(exc_info.value)


def test_raises_no_exception():
    with pytest.raises(ValueError):
        pass  # This test FAILS — no exception was raised
```

## warns — Warning Testing

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pytest warns warning](https://realpython.com/search?q=pytest+warns+warning).
:::

Verify that code emits expected warnings.

```python
import pytest
import warnings


def test_warns():
    with pytest.warns(UserWarning, match="deprecated"):
        warnings.warn("This function is deprecated", UserWarning)


def test_warns_no_warning():
    with pytest.warns(None):
        "safe operation"


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_ignore_warning():
    warnings.warn("deprecated", DeprecationWarning)
    # Warning is suppressed
```

## Filtering Tests with -k and -m

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on filtering tests with -k and -m](https://realpython.com/search?q=filtering+tests+with+-k+and+-m).
:::

Select which tests to run using keyword expressions and marks.

```bash
# Run tests by keyword
pytest -k "test_user"              # Tests with "test_user" in name
pytest -k "not test_slow"          # Skip slow tests
pytest -k "test_login or test_api" # Run either

# Custom marks
pytest -m "slow"                   # Only @pytest.mark.slow tests
pytest -m "not slow"               # Skip slow tests
pytest -m "regression"             # Only regression tests
```

```python
import pytest


@pytest.mark.slow
def test_heavy_computation():
    import time
    time.sleep(5)
    assert True


@pytest.mark.regression
def test_regression_fix():
    assert True


@pytest.mark.smoke
def test_smoke():
    assert True
```

## Debugging with --pdb and --trace

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on debugging with --pdb and --trace](https://realpython.com/search?q=debugging+with+--pdb+and+--trace).
:::

Drop into the debugger on test failure or at a specific point.

```bash
# Drop into pdb on first failure
pytest --pdb

# Drop into pdb on any failure (not just first)
pytest --pdb --pdbcls=IPython.terminal.debugger.TerminalDebugger

# Run to a specific line and break
pytest --trace
```

```python
# Use pytest.set_trace() to break at a specific point
def test_debug():
    x = 1
    y = 2
    pytest.set_trace()  # Breaks into debugger here
    assert x + y == 3
```

## References

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest parametrize](https://docs.pytest.org/en/stable/parametrize.html)
- [pytest built-in fixtures](https://docs.pytest.org/en/stable/reference/fixtures.html)
