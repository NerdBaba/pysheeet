---
title: Unittest Mock
---

# Unittest Mock

Source  
[src/basic/unittest_mock_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/unittest_mock_.py)

[[toc]]

Python's `unittest.mock` module provides powerful tools for replacing parts of your system under test with mock objects and making assertions about how they were used. It's essential for isolating code from external dependencies like databases, HTTP APIs, file systems, and random number generators. The module is part of the standard library (Python 3.3+), available as `from unittest.mock import ...`.

## Mock and MagicMock

`Mock` is a flexible fake object that records how it's called. `MagicMock` extends Mock with pre-defined implementations of Python's magic methods (`__len__`, `__str__`, `__iter__`, etc.).

```python
from unittest.mock import Mock, MagicMock

# Basic mock — any attribute access returns another Mock
m = Mock()
print(m.some_method())        # <Mock name='mock.some_method()' ...>
print(m.arbitrary_attribute)  # <Mock name='mock.arbitrary_attribute' ...>

# MagicMock — supports magic methods
mm = MagicMock()
mm.__len__.return_value = 42
print(len(mm))               # 42
mm.__str__.return_value = "magic!"
print(str(mm))               # magic!

# Iterable magic mock
mm.__iter__.return_value = iter([1, 2, 3])
print(list(mm))              # [1, 2, 3]
```

## return_value and side_effect

Control what a mock returns or does when called.

```python
from unittest.mock import Mock

# Fixed return value
m = Mock(return_value=42)
print(m())      # 42

# Set after creation
m.return_value = 100
print(m())      # 100

# side_effect — raises exception
m = Mock(side_effect=ValueError("bad"))
# m()  # Raises ValueError

# side_effect — different values per call
m = Mock(side_effect=[1, 2, 3, StopIteration])
print(m())      # 1
print(m())      # 2
print(m())      # 3
# m()           # Raises StopIteration

# side_effect — function called with args
def side_effect(*args, **kwargs):
    return sum(args)

m = Mock(side_effect=side_effect)
print(m(1, 2, 3))  # 6

# side_effect and return_value together
m.side_effect = None  # Reset to use return_value
m.return_value = 99
print(m())            # 99
```

## Asserting Calls

Mock records every call. Use assertion methods to verify behavior.

```python
from unittest.mock import Mock

m = Mock()

m(1, 2, key="value")
m(3, 4)

# Assert call with specific args
m.assert_called_with(3, 4)               # Last call matches
m.assert_called_once_with(1, 2, key="value")  # Only one call total

# Assert at least one call
m.assert_called()

# Assert any call matches
m.assert_any_call(1, 2, key="value")

# Assert NOT called
m.assert_not_called()

# Check call count
print(m.call_count)     # 2
print(m.called)         # True

# Inspect call history
print(m.call_args)          # Last call args
print(m.call_args_list)     # All calls as list
print(m.method_calls)       # All method calls on mock
```

## call and call_count

`call` is a helper for constructing call tuples. Use it to compare against `call_args_list`.

```python
from unittest.mock import Mock, call

m = Mock()
m(1)
m(2, 3)
m(key="value")

# Build expected call list
expected = [call(1), call(2, 3), call(key="value")]
assert m.call_args_list == expected

# call_count
assert m.call_count == 3

# Nested calls — attribute access
m.hello("world")
m.hello.assert_called_with("world")
print(m.method_calls)  # [call.hello('world')]
```

## patch — Decorator and Context Manager

`patch` replaces real objects with mocks during a test. Use as a decorator or context manager.

```python
import os
from unittest.mock import patch


# As decorator — mock is injected as argument
@patch("os.listdir")
@patch("os.path.exists")
def test_files(mock_exists, mock_listdir):
    mock_listdir.return_value = ["file1.txt", "file2.txt"]
    mock_exists.return_value = True

    result = os.listdir(".")
    assert result == ["file1.txt", "file2.txt"]
    assert os.path.exists("anything")


# As context manager
def test_with_context():
    with patch("os.getcwd") as mock_getcwd:
        mock_getcwd.return_value = "/fake/path"
        assert os.getcwd() == "/fake/path"


# Patch string in module (not import location!)
# In mymodule.py: from os import getcwd -> patch("os.getcwd")
# In mymodule.py: import os -> patch("mymodule.os.getcwd")
```

::: warning
Patch where the object is **used** (looked up), not where it's defined. If `mymodule.py` does `from os import getcwd`, patch `"mymodule.getcwd"`, not `"os.getcwd"`.
:::

## patch.object, patch.multiple, patch.dict

More specific patch variants for targeted replacements.

```python
from unittest.mock import patch, Mock
import os


class MyClass:
    def method(self):
        return "real"


# patch.object — replace method on a class
with patch.object(MyClass, "method", return_value="mocked"):
    obj = MyClass()
    print(obj.method())  # "mocked"


# patch.object with autospec
with patch.object(MyClass, "method", autospec=True) as mock_method:
    mock_method.return_value = "mocked"
    obj = MyClass()
    print(obj.method())  # "mocked"


# patch.multiple — patch several attributes at once
with patch.multiple(
    "os.path",
    exists=Mock(return_value=True),
    isfile=Mock(return_value=True),
):
    assert os.path.exists("/any") is True
    assert os.path.isfile("/any") is True


# patch.dict — modify a dictionary temporarily
config = {"host": "localhost", "port": 8080}

with patch.dict(config, {"host": "staging.example.com"}):
    assert config["host"] == "staging.example.com"

assert config["host"] == "localhost"  # Restored after context


# patch.dict — add/clear dictionary
with patch.dict(config, {"debug": "true"}, clear=True):
    assert config == {"debug": "true"}
```

## patch.dict with os.environ

Temporarily modify environment variables using `patch.dict("os.environ", ...)`.

```python
import os
from unittest.mock import patch

with patch.dict("os.environ", {"DATABASE_URL": "sqlite:///test.db"}):
    assert os.environ["DATABASE_URL"] == "sqlite:///test.db"

assert "DATABASE_URL" not in os.environ  # Restored

# Add multiple env vars
with patch.dict("os.environ", {
    "DB_HOST": "localhost",
    "DB_PORT": "5432",
}, clear=True):
    pass  # Only those vars exist in os.environ
```

## PropertyMock

Mock a property on a class. Set the return value on the mock instance.

```python
from unittest.mock import PropertyMock, patch


class MyClass:
    @property
    def status(self):
        return "active"


with patch.object(MyClass, "status", new_callable=PropertyMock) as mock_status:
    mock_status.return_value = "inactive"
    obj = MyClass()
    print(obj.status)  # "inactive"

    # Change return value during test
    mock_status.return_value = "error"
    print(obj.status)  # "error"


# Alternative: set as class attribute on mock
mock = PropertyMock(return_value="inactive")
with patch.object(MyClass, "status", mock, create=True):
    obj = MyClass()
    print(obj.status)  # "inactive"
```

## AsyncMock

Mock async functions and methods (Python 3.8+).

```python
import pytest
from unittest.mock import AsyncMock, patch


class AsyncClient:
    async def fetch_data(self):
        return {"data": "real"}


@pytest.mark.asyncio
async def test_async():
    mock = AsyncMock(return_value={"data": "mocked"})

    # Use with patch
    with patch.object(AsyncClient, "fetch_data", mock):
        client = AsyncClient()
        result = await client.fetch_data()
        assert result == {"data": "mocked"}

    # AsyncMock tracks await count
    mock.assert_awaited_once()
    mock.assert_awaited_with()


# AsyncMock with side_effect
async def test_async_side_effect():
    mock = AsyncMock(side_effect=[ValueError("first"), {"ok": True}])

    with pytest.raises(ValueError):
        await mock()

    result = await mock()
    assert result == {"ok": True}


# Mocking async context manager
@pytest.mark.asyncio
async def test_async_context_manager():
    mock = AsyncMock()
    mock.__aenter__.return_value = {"db": "connected"}
    mock.__aexit__.return_value = None

    async with mock as conn:
        assert conn == {"db": "connected"}
```

## mock_open — File Mocking

Replace the built-in `open()` function to test file reading and writing without real filesystem access.

```python
from unittest.mock import mock_open, patch
import json


def read_config(path):
    with open(path) as f:
        return json.load(f)


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_read_config(mock_file):
    result = read_config("/fake/path.json")
    assert result == {"key": "value"}
    mock_file.assert_called_with("/fake/path.json")


# Testing file write
@patch("builtins.open", new_callable=mock_open)
def test_write_file(mock_file):
    with open("output.txt", "w") as f:
        f.write("hello\n")
        f.write("world\n")

    # Check handle calls
    handle = mock_file()
    handle.write.assert_any_call("hello\n")
    handle.write.assert_any_call("world\n")
```

## ANY — Match Anything

`ANY` matches any value for an argument. Useful when you don't care about specific parameters.

```python
from unittest.mock import ANY, Mock

m = Mock()
m(1, "hello", key={"nested": "dict"})

# Match with ANY for parts we don't care about
m.assert_called_with(1, ANY, key=ANY)


# In assertions with specific and ANY arguments
m.assert_called_with(ANY, "hello", key={"nested": "dict"})


# Compare actual call to expected with ANY
from unittest.mock import call
m(42, debug=True)
m.assert_has_calls([
    call(1, "hello", key=ANY),
    call(ANY, debug=True),
])
```

## create_autospec — Signature Matching

Create a mock that matches the original object's signature. Calling the mock with wrong arguments raises `TypeError`, preventing tests that pass with invalid calls.

```python
from unittest.mock import create_autospec


def real_function(a, b, c=3):
    return a + b + c


# Autospec preserves signature
mock = create_autospec(real_function, return_value=10)

print(mock(1, 2))           # 10
print(mock(1, 2, c=5))      # 10

# Raises TypeError: missing required arg
# mock(1)

# Raises TypeError: unexpected keyword
# mock(1, 2, unknown=True)


class MyClass:
    def instance_method(self, x, y):
        return x + y


# Autospec on class methods
mock_obj = create_autospec(MyClass)
# mock_obj.instance_method(1)  # TypeError: missing y
mock_obj.instance_method(1, 2)  # OK

# Strict mode — rejects unexpected attributes
# mock_obj.unexpected  # AttributeError
```

## References

- [unittest.mock — Mock object library](https://docs.python.org/3/library/unittest.mock.html)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [Mock example recipes](https://docs.python.org/3/library/unittest.mock-examples.html)
