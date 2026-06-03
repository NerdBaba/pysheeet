---
title: Functools
---

# Functools

[[toc]]
The `functools` module provides higher-order functions that act on or return other functions. It includes tools for partial application, caching, type-based dispatch, and decorator utilities that make Python code more modular and reusable. This cheat sheet covers the most useful functions for everyday development.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/functools.py).

## References

- [functools — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html)
- [PEP 443 — Single-dispatch generic functions](https://www.python.org/dev/peps/pep-0443/)
- [PEP 257 — Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)

## `partial` — Pre-fill Function Arguments

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on partial functools python](https://realpython.com/search?q=partial+functools+python).
:::


`partial` creates a new callable with some arguments of the original function pre-filled. This is useful for specializing general functions or preparing callback arguments.

```python
>>> from functools import partial

>>> def power(base, exponent):
...     return base ** exponent
...
>>> square = partial(power, exponent=2)
>>> cube = partial(power, exponent=3)
>>> square(5)
25
>>> cube(5)
125

>>> def log(level, message):
...     print(f"[{level}] {message}")
...
>>> info = partial(log, "INFO")
>>> warn = partial(log, "WARN")
>>> info("Server started")
[INFO] Server started
```

## `partialmethod` — Partial Methods for Classes

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on partialmethod functools python](https://realpython.com/search?q=partialmethod+functools+python).
:::


`partialmethod` behaves like `partial` but is designed for method definitions inside classes. It binds the given arguments at class definition time.

**New in Python 3.4**

```python
>>> from functools import partialmethod

>>> class Cell:
...     def __init__(self):
...         self.alive = False
...     def set_state(self, state):
...         self.alive = state
...     set_alive = partialmethod(set_state, True)
...     set_dead = partialmethod(set_state, False)
...
>>> c = Cell()
>>> c.set_alive()
>>> c.alive
True
```

## Caching: `lru_cache` and `cache`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on lru cache functools python](https://realpython.com/search?q=lru+cache+functools+python).
:::


Memoization decorators that automatically cache return values based on arguments.

```python
>>> from functools import lru_cache, cache

# lru_cache with maxsize — evicts least recently used entries
>>> @lru_cache(maxsize=128)
... def fib(n):
...     if n < 2:
...         return n
...     return fib(n - 1) + fib(n - 2)
...
>>> fib(100)
354224848179261915075
>>> fib.cache_info()
CacheInfo(hits=98, misses=101, maxsize=128, currsize=101)

# cache — unbounded, simpler alias for lru_cache(maxsize=None)
>>> @cache
... def factorial(n):
...     return n * factorial(n - 1) if n else 1
...
>>> factorial(20)
2432902008176640000

# typed — cache based on argument types separately (Python 3.3+)
>>> @lru_cache(typed=True)
... def f(x):
...     return x ** 2
...
# f(2) and f(2.0) are cached separately
```

::: warning
Cache arguments must be hashable. The cache lives for the lifetime of the process — use `cache_clear()` to reset. Do not use `lru_cache` on methods of mutable instances without careful consideration, as `self` is part of the cache key.
:::

## `singledispatch` — Type-Based Dispatch

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on singledispatch functools python](https://realpython.com/search?q=singledispatch+functools+python).
:::


`singledispatch` lets you define a generic function whose behavior depends on the type of the first argument.

**New in Python 3.4**

```python
>>> from functools import singledispatch
>>> from decimal import Decimal

>>> @singledispatch
... def process(arg):
...     raise TypeError(f"Unsupported type: {type(arg)}")
...
>>> @process.register(int)
... def _(arg):
...     return f"Integer: {arg * 2}"
...
>>> @process.register(str)
... def _(arg):
...     return f"String: {arg.upper()}"
...
>>> @process.register(list)
... def _(arg):
...     return [process(x) for x in arg]
...
>>> @process.register(Decimal)
... def _(arg):
...     return f"Decimal: {arg ** 2}"
...
>>> process(5)
'Integer: 10'
>>> process("hello")
'String: HELLO'
>>> process([1, 2, 3])
['Integer: 2', 'Integer: 4', 'Integer: 6']
```

## `wraps` and `WRAPPER_ASSIGNMENTS` — Decorator Hygiene

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on wraps functools python decorator](https://realpython.com/search?q=wraps+functools+python+decorator).
:::


`wraps` copies the original function's `__name__`, `__doc__`, `__module__`, `__annotations__`, and `__qualname__` to the wrapper function.

```python
>>> from functools import wraps, WRAPPER_ASSIGNMENTS

>>> WRAPPER_ASSIGNMENTS
('__module__', '__name__', '__qualname__', '__annotations__', '__doc__')

>>> def without_wraps(func):
...     def wrapper(*args, **kwargs):
...         return func(*args, **kwargs)
...     return wrapper
...
>>> def with_wraps(func):
...     @wraps(func)
...     def wrapper(*args, **kwargs):
...         return func(*args, **kwargs)
...     return wrapper
...
>>> @without_wraps
... def example():
...     """Docstring."""
...     pass
...
>>> example.__name__
'wrapper'

>>> @with_wraps
... def example():
...     """Docstring."""
...     pass
...
>>> example.__name__
'example'
>>> example.__doc__
'Docstring.'
```

## `reduce` — Cumulative Reduction

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on reduce functools python](https://realpython.com/search?q=reduce+functools+python).
:::


`reduce` applies a binary function cumulatively, reducing an iterable to a single value.

```python
>>> from functools import reduce

>>> reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
120

>>> reduce(lambda x, y: x + y, ["A", "B", "C"])
'ABC'

# with initial value
>>> reduce(lambda x, y: x + y, [1, 2, 3], 10)
16
```

## `cmp_to_key` — Convert Comparison to Key Function

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cmp to key functools python](https://realpython.com/search?q=cmp+to+key+functools+python).
:::


Converts an old-style comparison function (returning -1, 0, 1) into a key function for `sorted()`, `min()`, `max()`.

```python
>>> from functools import cmp_to_key

>>> def compare(x, y):
...     if x < y: return -1
...     if x > y: return 1
...     return 0
...
>>> sorted([3, 1, 4, 1, 5], key=cmp_to_key(compare))
[1, 1, 3, 4, 5]

# custom sort by length then alphabetically
>>> def len_then_alpha(a, b):
...     if len(a) != len(b):
...         return -1 if len(a) < len(b) else 1
...     return -1 if a < b else 1 if a > b else 0
...
>>> words = ["banana", "apple", "cherry", "date"]
>>> sorted(words, key=cmp_to_key(len_then_alpha))
['date', 'apple', 'banana', 'cherry']
```

## `total_ordering` — Auto-Generate Comparison Methods

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on total ordering functools python](https://realpython.com/search?q=total+ordering+functools+python).
:::


`total_ordering` fills in missing rich comparison methods (`__le__`, `__gt__`, `__ge__`) given at least `__eq__` and one of `__lt__`, `__le__`, `__gt__`, or `__ge__`.

```python
>>> from functools import total_ordering

>>> @total_ordering
... class Version:
...     def __init__(self, major, minor):
...         self.major = major
...         self.minor = minor
...     def __eq__(self, other):
...         return (self.major, self.minor) == (other.major, other.minor)
...     def __lt__(self, other):
...         return (self.major, self.minor) < (other.major, other.minor)
...
>>> v1 = Version(2, 1)
>>> v2 = Version(3, 0)
>>> v1 < v2
True
>>> v1 <= v2
True
>>> v1 > v2
False
```
