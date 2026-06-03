---
title: Testing
---

# Testing

[[toc]]

Testing is a critical practice in professional Python development. Python's standard library includes `unittest` and `unittest.mock` for writing and isolating tests, while `pytest` has become the de facto standard for its concise syntax, powerful fixtures, and extensive plugin ecosystem.

This section covers testing patterns that help you write reliable, maintainable tests for your Python code.

## Topics

- **[Pytest](/testing/python-pytest)** — Fixtures, parametrize, built-in fixtures (`tmp_path`, `monkeypatch`), assertion introspection, `raises`/`warns`
- **[Unittest Mock](/testing/python-unittest-mock)** — `Mock`/`MagicMock`, `patch` (decorator & context manager), `AsyncMock`, `mock_open`, `create_autospec`

## References

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock — Mock object library](https://docs.python.org/3/library/unittest.mock.html)
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
