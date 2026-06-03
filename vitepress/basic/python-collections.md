---
title: Collections
---

# Collections

[[toc]]
The `collections` module provides specialized container datatypes that extend Python's built-in types (`dict`, `list`, `set`, `str`) with additional functionality. Whether you need an ordered dictionary, a double-ended queue, a counting hash, or a dictionary with automatic default values, `collections` has a well-tested, performant alternative. This cheat sheet covers the most useful containers and their practical applications.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/collections.py).

## References

- [collections — Container datatypes](https://docs.python.org/3/library/collections.html)
- [collections.abc — Abstract Base Classes for Containers](https://docs.python.org/3/library/collections.abc.html)
- [PEP 372 — Adding an ordered dictionary to collections](https://www.python.org/dev/peps/pep-0372/)

## `namedtuple` — Lightweight Immutable Data Containers

`namedtuple` creates tuple-like classes with named fields, combining the immutability and memory efficiency of tuples with the readability of object attribute access.

```python
>>> from collections import namedtuple

>>> Point = namedtuple("Point", ["x", "y"])
>>> p = Point(10, y=20)
>>> p.x, p.y, p[0], p[1]
(10, 20, 10, 20)
>>> x, y = p  # unpacking works
>>> str(p)
'Point(x=10, y=20)'
```

### Defaults and Rename

```python
# defaults (Python 3.7+) — applied to rightmost fields
>>> Person = namedtuple("Person", ["name", "age", "city"], defaults=["NYC"])
>>> Person("Alice", 30)
Person(name='Alice', age=30, city='NYC')

# rename — auto-rename invalid field names
>>> Fields = namedtuple("Fields", ["abc", "def", "class"], rename=True)
>>> Fields._fields
('abc', '_1', '_2')

# _asdict() returns an OrderedDict
>>> p = Point(3, 4)
>>> p._asdict()
{'x': 3, 'y': 4}

# _replace() creates a new instance with changed fields
>>> p._replace(x=5)
Point(x=5, y=4)
```

::: warning
`namedtuple` fields are accessible as attributes, but the underlying storage is a tuple — you cannot add or remove fields after creation. Use `dataclasses` (Python 3.7+) if you need mutable data or default factories.
:::

## `deque` — Double-Ended Queue

`deque` (pronounced "deck") is optimized for fast appends and pops from both ends with O(1) performance, contrasted with `list` which is O(n) for left-side operations.

```python
>>> from collections import deque

>>> d = deque([1, 2, 3])
>>> d.append(4)         # right side
>>> d.appendleft(0)     # left side
>>> d.pop()             # 4
>>> d.popleft()         # 0
>>> d
deque([1, 2, 3])

# maxlen — bounded deque (circular buffer)
>>> d = deque(maxlen=3)
>>> for i in range(5): d.append(i)
...
>>> d
deque([2, 3, 4], maxlen=3)

# rotate — shift elements right (positive) or left (negative)
>>> d = deque([1, 2, 3, 4, 5])
>>> d.rotate(2)
>>> d
deque([4, 5, 1, 2, 3])
>>> d.rotate(-1)
>>> d
deque([5, 1, 2, 3, 4])

# efficient tail implementation
>>> def tail(filename, n=10):
...     with open(filename) as f:
...         return deque(f, n)
```

## `Counter` — Multiset / Bag

`Counter` is a dict subclass for counting hashable objects. It provides arithmetic operations and common counting idioms.

```python
>>> from collections import Counter

>>> words = ["a", "b", "a", "c", "b", "a"]
>>> cnt = Counter(words)
>>> cnt
Counter({'a': 3, 'b': 2, 'c': 1})

# most_common — top N elements
>>> cnt.most_common(2)
[('a', 3), ('b', 2)]

# arithmetic
>>> c1 = Counter(a=3, b=1)
>>> c2 = Counter(a=1, b=2)
>>> c1 + c2
Counter({'a': 4, 'b': 3})
>>> c1 - c2  # only keeps positive counts
Counter({'a': 2})
>>> c1 & c2  # intersection (min)
Counter({'a': 1, 'b': 1})
>>> c1 | c2  # union (max)
Counter({'a': 3, 'b': 2})

# update and subtract
>>> cnt = Counter(a=3, b=1)
>>> cnt.update(a=1, c=2)
>>> cnt
Counter({'a': 4, 'c': 2, 'b': 1})
>>> cnt.subtract(a=2)
>>> cnt
Counter({'a': 2, 'c': 2, 'b': 1})
```

## `defaultdict` — Dictionary with Default Factory

`defaultdict` calls a factory function to supply missing keys, eliminating the need for explicit checks.

```python
>>> from collections import defaultdict

# default_factory=int — count items
>>> cnt = defaultdict(int)
>>> for word in ["a", "b", "a"]:
...     cnt[word] += 1
...
>>> dict(cnt)
{'a': 2, 'b': 1}

# default_factory=list — group items
>>> groups = defaultdict(list)
>>> for key, val in [("a", 1), ("b", 2), ("a", 3)]:
...     groups[key].append(val)
...
>>> dict(groups)
{'a': [1, 3], 'b': [2]}

# default_factory=set — deduplicate
>>> uniq = defaultdict(set)
>>> for key, val in [("a", 1), ("a", 1), ("b", 2)]:
...     uniq[key].add(val)
...
>>> dict(uniq)
{'a': {1}, 'b': {2}}

# custom factory
>>> from functools import partial
>>> defaultdict(partial(dict, {"default": 42}))["missing"]
{'default': 42}

# nested defaultdict
>>> nested = defaultdict(lambda: defaultdict(list))
>>> nested["x"]["y"].append(1)
>>> nested["x"]["y"]
[1]
```

::: warning
Accessing a missing key with `defaultdict` creates the default value as a side effect — unlike `dict.get()` or `dict.setdefault()`. Use `d.get(key)` only if you want to avoid creating entries.
:::

## `OrderedDict` — Dictionary with Ordered Keys

`OrderedDict` remembers insertion order. Since Python 3.7, regular `dict` also preserves insertion order, but `OrderedDict` provides additional methods.

```python
>>> from collections import OrderedDict

>>> d = OrderedDict()
>>> d["a"] = 1
>>> d["b"] = 2
>>> d["c"] = 3
>>> d
OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# move_to_end — move key to front (last=True) or back (last=False)
>>> d.move_to_end("a")
>>> list(d.keys())
['b', 'c', 'a']
>>> d.move_to_end("a", last=False)
>>> list(d.keys())
['a', 'b', 'c']

# popitem — FIFO (last=True) or LIFO (last=False)
>>> d.popitem(last=True)   # last item (LIFO)
('c', 3)
>>> d.popitem(last=False)  # first item (FIFO)
('a', 1)

# equality is order-sensitive
>>> OrderedDict(a=1, b=2) == OrderedDict(b=2, a=1)
False
>>> OrderedDict(a=1, b=2) == {"a": 1, "b": 2}
True  # equal to regular dict ignores order
```

## `ChainMap` — Merging Multiple Dictionaries

`ChainMap` groups multiple dicts (or other mappings) into a single view. Lookups search each mapping in order, while writes affect the first mapping.

```python
>>> from collections import ChainMap

>>> defaults = {"theme": "dark", "lang": "en"}
>>> user_prefs = {"lang": "fr", "font_size": 14}
>>> session = {"lang": "de"}

>>> config = ChainMap(session, user_prefs, defaults)
>>> config["lang"]
'de'            # from session
>>> config["font_size"]
14              # from user_prefs
>>> config["theme"]
'dark'          # from defaults

# new_child — add a mapping to the front
>>> config = config.new_child({"lang": "es"})
>>> config["lang"]
'es'

# maps — access the list of underlying mappings
>>> config.maps
[{'lang': 'es'}, {'lang': 'de'}, {'lang': 'fr', 'font_size': 14}, {'theme': 'dark', 'lang': 'en'}]
```

## `UserDict`, `UserList`, `UserString` — Easy Subclassing

These classes wrap the built-in types and are designed for subclassing, providing a simpler alternative to inheriting from `dict`, `list`, or `str` directly.

```python
>>> from collections import UserDict, UserList, UserString

# UserDict — subclass dict with custom behavior
>>> class CaseInsensitiveDict(UserDict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key.lower(), value)
...     def __getitem__(self, key):
...         return super().__getitem__(key.lower())
...
>>> d = CaseInsensitiveDict()
>>> d["Hello"] = "World"
>>> d["hello"]
'World'

# UserList — subclass list with custom behavior
>>> class DefaultList(UserList):
...     def __init__(self, initlist=None, default=0):
...         super().__init__(initlist)
...         self.default = default
...     def __getitem__(self, index):
...         try:
...             return super().__getitem__(index)
...         except IndexError:
...             return self.default
...
>>> dl = DefaultList([1, 2, 3])
>>> dl[5]
0

# UserString — subclass str with custom behavior
>>> class PrefixString(UserString):
...     def __init__(self, seq, prefix=">> "):
...         super().__init__(seq)
...         self.prefix = prefix
...     def __repr__(self):
...         return f"{self.prefix}{super().__repr__()}"
...
>>> print(PrefixString("hello"))
>> hello
```
