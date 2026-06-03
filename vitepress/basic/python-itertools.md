---
title: Itertools
---

# Itertools

[[toc]]
The `itertools` module is a collection of fast, memory-efficient tools for working with iterators. It provides building blocks for constructing specialized iterator patterns — infinite sequences, combinatorics, grouping, slicing, and chaining — without storing intermediate results in memory. This cheat sheet covers the most commonly used functions, from infinite iterators to combinatorial generators.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/itertools.py).

## References

- [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html)
- [More Itertools](https://more-itertools.readthedocs.io/)
- [Python itertools — Effective Python](https://realpython.com/python-itertools/)

## Infinite Iterators: `count`, `cycle`, `repeat`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on infinite iterators count cycle repeat](https://realpython.com/search?q=infinite+iterators+count+cycle+repeat).
:::


Infinite iterators generate an unbounded sequence of values. Use them with care — always pair with `islice` or a `break` condition to avoid infinite loops.

```python
>>> from itertools import count, cycle, repeat, islice

# count(start=0, step=1) — endless arithmetic progression
>>> list(islice(count(10, 2.5), 5))
[10, 12.5, 15.0, 17.5, 20.0]

# cycle(iterable) — endlessly repeat an iterable
>>> list(islice(cycle("AB"), 6))
['A', 'B', 'A', 'B', 'A', 'B']

# repeat(object[, times]) — repeat a single value
>>> list(repeat(42, 4))
[42, 42, 42, 42]
```

## Chaining Iterators: `chain`, `chain.from_iterable`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on chaining iterators chain chain from_iterable](https://realpython.com/search?q=chaining+iterators+chain+chain+from_iterable).
:::


`chain` concatenates multiple iterables into a single sequence without creating a new list. `chain.from_iterable` is useful when the sources are themselves in an iterable.

```python
>>> from itertools import chain

>>> list(chain([1, 2], "AB", range(3)))
[1, 2, 'A', 'B', 0, 1, 2]

>>> chunks = [[1, 2], [3, 4], [5]]
>>> list(chain.from_iterable(chunks))
[1, 2, 3, 4, 5]

# flatten a nested list
>>> nested = [[1, 2], [3], [4, 5, 6]]
>>> list(chain.from_iterable(nested))
[1, 2, 3, 4, 5, 6]
```

## Filtering Iterators: `compress`, `dropwhile`, `takewhile`, `filterfalse`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on filtering iterators compress dropwhile takewhile filterfalse](https://realpython.com/search?q=filtering+iterators+compress+dropwhile+takewhile+filterfalse).
:::


These functions filter elements from an iterable based on different criteria.

```python
>>> from itertools import compress, dropwhile, takewhile, filterfalse

# compress(data, selectors) — filter by boolean selector
>>> list(compress("ABCDEF", [1, 0, 1, 0, 1, 0]))
['A', 'C', 'E']

# dropwhile(predicate, iterable) — drop elements while True, then yield rest
>>> list(dropwhile(lambda x: x < 5, [1, 4, 6, 3, 8]))
[6, 3, 8]

# takewhile(predicate, iterable) — yield elements while True, then stop
>>> list(takewhile(lambda x: x < 5, [1, 4, 6, 3, 8]))
[1, 4]

# filterfalse(predicate, iterable) — yield elements where predicate is False
>>> list(filterfalse(lambda x: x % 2, range(10)))
[0, 2, 4, 6, 8]
```

## Slicing and Windowing: `islice`, `pairwise`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on slicing and windowing islice pairwise](https://realpython.com/search?q=slicing+and+windowing+islice+pairwise).
:::


`islice` performs lazy slicing on any iterable. `pairwise` yields consecutive overlapping pairs.

```python
>>> from itertools import islice, pairwise

# islice(iterable, start, stop[, step])
>>> list(islice(range(10), 2, 8, 2))
[2, 4, 6]

>>> data = [1, 2, 3, 4, 5]
>>> list(pairwise(data))
[(1, 2), (2, 3), (3, 4), (4, 5)]

# sliding window of size 3 using islice + zip
>>> def sliding_window(iterable, n):
...     iterators = [islice(iterable, i, None) for i in range(n)]
...     return zip(*iterators)
...
>>> list(sliding_window([1, 2, 3, 4, 5], 3))
[(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

## Reducing Iterators: `accumulate`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on reducing iterators accumulate](https://realpython.com/search?q=reducing+iterators+accumulate).
:::


`accumulate` yields running sums (or other binary operations) from left to right.

```python
>>> from itertools import accumulate
>>> import operator

>>> list(accumulate([1, 2, 3, 4, 5]))
[1, 3, 6, 10, 15]

>>> list(accumulate([1, 2, 3, 4, 5], operator.mul))
[1, 2, 6, 24, 120]

>>> list(accumulate([3, 1, 4, 1, 5], max))
[3, 3, 4, 4, 5]
```

## Grouping: `groupby`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on grouping groupby](https://realpython.com/search?q=grouping+groupby).
:::


`groupby` groups consecutive elements with the same key. The input should be sorted by the key for meaningful results.

```python
>>> from itertools import groupby

>>> data = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]
>>> for key, group in groupby(data, lambda x: x[0]):
...     print(key, list(group))
...
a [('a', 1), ('a', 2)]
b [('b', 3), ('b', 4)]

# run-length encoding
>>> s = "AAABBCCCC"
>>> [(k, len(list(g))) for k, g in groupby(s)]
[('A', 3), ('B', 2), ('C', 4)]
```

::: warning
`groupby` groups only consecutive elements. If identical keys are not adjacent, they produce separate groups. Always sort by the key first if you want all same-key items grouped together.
:::

## Batching: `batched`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on batching batched](https://realpython.com/search?q=batching+batched).
:::


`batched` splits an iterable into fixed-size non-overlapping tuples.

**New in Python 3.12**

```python
>>> from itertools import batched

>>> list(batched(range(10), 3))
[(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]
```

## Combinatorial Iterators: `product`, `permutations`, `combinations`, `combinations_with_replacement`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on combinatorial iterators product permutations combinations combinations_with_replacement](https://realpython.com/search?q=combinatorial+iterators+product+permutations+combinations+combinations_with_replacement).
:::


These generate Cartesian products and combinations without building the entire result in memory.

```python
>>> from itertools import product, permutations, combinations, combinations_with_replacement

# cartesian product
>>> list(product("AB", range(2)))
[('A', 0), ('A', 1), ('B', 0), ('B', 1)]

>>> list(product("AB", repeat=2))
[('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]

# permutations — order matters, no repeats
>>> list(permutations("ABC", 2))
[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# combinations — order doesn't matter, no repeats
>>> list(combinations("ABC", 2))
[('A', 'B'), ('A', 'C'), ('B', 'C')]

# combinations with replacement — order doesn't matter, repeats allowed
>>> list(combinations_with_replacement("ABC", 2))
[('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]
```

## Mapping: `starmap`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on mapping starmap](https://realpython.com/search?q=mapping+starmap).
:::


`starmap` is like `map` but unpacks arguments from each tuple.

```python
>>> from itertools import starmap

>>> list(starmap(pow, [(2, 5), (3, 2), (4, 3)]))
[32, 9, 64]

>>> list(starmap(lambda x, y: x + y, [(1, 2), (3, 4)]))
[3, 7]
```

## Teeing: `tee`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on teeing tee](https://realpython.com/search?q=teeing+tee).
:::


`tee` splits a single iterator into multiple independent iterators. Each can be consumed separately, but they share memory for elements that haven't been consumed by all.

```python
>>> from itertools import tee

>>> it1, it2 = tee(range(5), 2)
>>> list(it1)
[0, 1, 2, 3, 4]
>>> list(it2)  # independent, starts from beginning
[0, 1, 2, 3, 4]
```

::: warning
After creating `tee` iterators, do not use the original iterator. Doing so can cause the tee'd iterators to silently advance out of sync.
:::

## Zipping: `zip_longest`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on zipping zip_longest](https://realpython.com/search?q=zipping+zip_longest).
:::


`zip_longest` zips iterables, filling missing values with a `fillvalue` instead of stopping at the shortest.

```python
>>> from itertools import zip_longest

>>> list(zip_longest("AB", "XYZ", fillvalue="?"))
[('A', 'X'), ('B', 'Y'), ('?', 'Z')]

# transpose uneven rows
>>> rows = [[1, 2], [3, 4, 5], [6]]
>>> list(zip_longest(*rows, fillvalue=0))
[(1, 3, 6), (2, 4, 0), (0, 5, 0)]
```
