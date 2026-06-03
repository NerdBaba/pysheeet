---
title: Profiling & Performance
---

# Profiling & Performance

[[toc]]
Profiling is the process of measuring where your program spends its time and memory. Python provides several tools — from simple timing utilities to statistical profilers — to help identify bottlenecks. This cheat sheet covers the most effective profiling tools and common optimization patterns.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/profiling.py).

## References

- [time — Time access and conversions](https://docs.python.org/3/library/time.html)
- [timeit — Measure execution time of small code snippets](https://docs.python.org/3/library/timeit.html)
- [The Python Profilers](https://docs.python.org/3/library/profile.html)
- [py-spy — Sampling profiler for Python programs](https://github.com/benfred/py-spy)
- [memory_profiler](https://pypi.org/project/memory-profiler/)
- [line_profiler](https://pypi.org/project/line-profiler/)

## Simple Timing with `time.perf_counter`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on simple timing with time perf_counter](https://realpython.com/search?q=simple+timing+with+time+perf_counter).
:::


For quick, ad-hoc timing of code blocks, `perf_counter` provides the highest available resolution clock.

```python
>>> import time

>>> def slow_function():
...     total = 0
...     for i in range(10_000_000):
...         total += i ** 2
...     return total
...
>>> start = time.perf_counter()
>>> result = slow_function()
>>> elapsed = time.perf_counter() - start
>>> print(f"Took {elapsed:.3f} seconds")
Took 0.184 seconds
```

## Micro-Benchmarks with `timeit`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on micro-benchmarks with timeit](https://realpython.com/search?q=micro-benchmarks+with+timeit).
:::


The `timeit` module measures execution time of small code snippets, running them many times for statistical accuracy. It disables the garbage collector during runs.

```python
>>> import timeit

# measure a statement
>>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
0.3413

# measure with setup
>>> timeit.timeit('sqrt(2)', 'from math import sqrt', number=100000)
0.0211

# compare approaches
>>> timeit.timeit('[]', number=10_000_000)
0.337
>>> timeit.timeit('list()', number=10_000_000)
0.517

# from the command line
# $ python -m timeit -s "from math import sqrt" "sqrt(2)"
```

## Function-Level Profiling with `cProfile` and `pstats`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on function-level profiling with cprofile and pstats](https://realpython.com/search?q=function-level+profiling+with+cprofile+and+pstats).
:::


`cProfile` records every function call and returns detailed statistics. `pstats` sorts and filters the results.

```python
>>> import cProfile, pstats

>>> def expensive():
...     total = 0
...     for i in range(1_000_000):
...         total += i ** 0.5
...     return total
...
>>> def run():
...     for _ in range(10):
...         expensive()
...
>>> profiler = cProfile.Profile()
>>> profiler.enable()
>>> run()
>>> profiler.disable()
>>> stats = pstats.Stats(profiler)
>>> stats.sort_stats("cumtime")
>>> stats.print_stats(5)

# from the command line
# $ python -m cProfile -s cumulative my_script.py
```

Common sort keys: `"cumtime"` (cumulative time), `"time"` (internal time), `"calls"`, `"ncalls"`.

## Visualizing Profiles with `snakeviz`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on visualizing profiles with snakeviz](https://realpython.com/search?q=visualizing+profiles+with+snakeviz).
:::


`snakeviz` provides an interactive flame chart visualization of `cProfile` output.

```bash
# install
$ pip install snakeviz

# profile a script and launch viewer
$ python -m cProfile -o output.prof my_script.py
$ snakeviz output.prof
```

## Memory Profiling with `memory_profiler`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on memory profiling with memory_profiler](https://realpython.com/search?q=memory+profiling+with+memory_profiler).
:::


`memory_profiler` measures memory usage line-by-line or over time. Use the `@profile` decorator to annotate functions of interest.

```bash
$ pip install memory_profiler
```

```python
>>> from memory_profiler import profile

>>> @profile
... def process():
...     a = [i for i in range(100_000)]
...     b = [i * 2 for i in a]
...     del a
...     c = [i ** 2 for i in b]
...     return c
...
>>> if __name__ == "__main__":
...     process()
```

Run with:

```bash
$ python -m memory_profiler script.py
```

## Line-Level Profiling with `line_profiler`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on line-level profiling with line_profiler](https://realpython.com/search?q=line-level+profiling+with+line_profiler).
:::


`line_profiler` measures time per line of code, which is invaluable for pinpointing bottlenecks inside functions.

```bash
$ pip install line_profiler
```

```python
>>> from line_profiler import line_profile

>>> @line_profile
... def compute():
...     total = 0
...     for i in range(1_000_000):
...         total += i ** 2
...         total -= i * 0.5
...     return total
...
>>> compute()
```

Run with:

```bash
$ kernprof -l -v script.py
```

## Sampling Profiler with `py-spy`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on sampling profiler with py-spy](https://realpython.com/search?q=sampling+profiler+with+py-spy).
:::


`py-spy` is a statistical (sampling) profiler that runs without modifying your code. It works on running processes and can profile production applications safely.

```bash
$ pip install py-spy

# profile a running process by PID
$ py-spy record -o profile.svg --pid 12345

# profile a script from start to finish
$ py-spy record -o profile.svg -- python my_script.py

# top-like live view
$ py-spy top --pid 12345
```

## Common Optimization Patterns

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on common optimization patterns](https://realpython.com/search?q=common+optimization+patterns).
:::


### List vs Generator

```python
# list comprehension — eager, more memory
>>> squares_list = [x ** 2 for x in range(1_000_000)]

# generator expression — lazy, memory-efficient
>>> squares_gen = (x ** 2 for x in range(1_000_000))
```

### Local Variable Binding

Looking up global or attribute names repeatedly is slower than using a local reference.

```python
>>> import math

>>> def slow(iterations):
...     total = 0.0
...     for i in range(iterations):
...         total += math.sqrt(i)  # global lookup each iteration
...     return total
...
>>> def fast(iterations):
...     total = 0.0
...     sqrt = math.sqrt  # local binding
...     for i in range(iterations):
...         total += sqrt(i)
...     return total
...
>>> timeit.timeit(lambda: slow(1_000_000), number=10)
1.478
>>> timeit.timeit(lambda: fast(1_000_000), number=10)
1.312
```

### `__slots__` — Reduce Memory per Instance

By default, instances store attributes in a per-instance `__dict__`. `__slots__` declares a fixed set of attributes stored in a tuple-like structure, saving memory and speeding attribute access.

```python
# without __slots__
>>> class Point:
...     def __init__(self, x, y):
...         self.x = x
...         self.y = y
...
>>> p = Point(1, 2)
>>> p.__dict__
{'x': 1, 'y': 2}

# with __slots__
>>> class SlotPoint:
...     __slots__ = ("x", "y")
...     def __init__(self, x, y):
...         self.x = x
...         self.y = y
...
>>> sp = SlotPoint(1, 2)
>>> # sp.__dict__  # AttributeError: 'SlotPoint' object has no attribute '__dict__'

# memory comparison
>>> import sys
>>> p = Point(1, 2)
>>> sp = SlotPoint(1, 2)
>>> sys.getsizeof(p) + sys.getsizeof(p.__dict__)
128
>>> sys.getsizeof(sp)
64
```

::: warning
`__slots__` prevents adding new attributes dynamically and breaks code that relies on `__dict__`. It is most beneficial when creating millions of instances. For dataclasses (Python 3.10+), use `@dataclass(slots=True)` instead.
:::

### Use Built-in Functions and Libraries

Python's built-in functions and standard library modules are implemented in C and are significantly faster than equivalent pure-Python loops.

```python
>>> from functools import reduce
>>> import operator

# pure Python
>>> def manual_sum(n):
...     total = 0
...     for i in range(n):
...         total += i
...     return total
...
>>> timeit.timeit(lambda: manual_sum(1_000_000), number=10)
0.452

# built-in sum (C implementation)
>>> timeit.timeit(lambda: sum(range(1_000_000)), number=10)
0.089

# reduce with operator.add
>>> timeit.timeit(lambda: reduce(operator.add, range(1_000_000)), number=10)
0.082
```
