---
title: Dataclasses
---

# Dataclasses

[[toc]]
Dataclasses, introduced in Python 3.7 via PEP 557, provide a decorator that automatically generates `__init__`, `__repr__`, `__eq__`, and other special methods for classes that primarily store data. They reduce boilerplate while remaining fully compatible with Python's type annotation system. This cheat sheet covers the full range of dataclass features, from basic usage to advanced patterns.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/dataclasses.py).

## References

- [dataclasses — Data Classes](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 — Data Classes](https://www.python.org/dev/peps/pep-0557/)
- [PEP 681 — Data Class Transforms](https://www.python.org/dev/peps/pep-0681/)

## Basic Dataclass

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic dataclass](https://realpython.com/search?q=basic+dataclass).
:::


A minimal dataclass requires only the decorator and type annotations. `__init__`, `__repr__`, and `__eq__` are generated automatically.

```python
>>> from dataclasses import dataclass

>>> @dataclass
... class Point:
...     x: float
...     y: float
...
>>> p = Point(1.0, 2.0)
>>> p
Point(x=1.0, y=2.0)
>>> p.x, p.y
(1.0, 2.0)
>>> Point(1.0, 2.0) == Point(1.0, 2.0)
True
```

## Default Values and `field()`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on default values and field](https://realpython.com/search?q=default+values+and+field).
:::


Default values can be assigned directly in the annotation. Use `field()` for more control — default factory functions, exclude from repr, or mark a field as not comparable.

```python
>>> from dataclasses import dataclass, field

>>> @dataclass
... class Config:
...     host: str = "localhost"
...     port: int = 8080
...     debug: bool = False
...
>>> Config()
Config(host='localhost', port=8080, debug=False)

# field() with default_factory for mutable defaults
>>> @dataclass
... class ShoppingCart:
...     items: list = field(default_factory=list)
...     discounts: set = field(default_factory=set)
...     metadata: dict = field(default_factory=dict)
...
>>> cart = ShoppingCart()
>>> cart.items.append("apple")
>>> cart
ShoppingCart(items=['apple'], discounts=set(), metadata={})

# field() options
>>> @dataclass
... class User:
...     id: int
...     name: str = field(compare=False)     # exclude from __eq__
...     password: str = field(repr=False)    # hide from __repr__
...     metadata: dict = field(default_factory=dict, hash=False)
...
>>> User(1, "alice", "secret")
User(id=1, name='alice')
```

::: warning
Never use mutable objects as direct default values — they are shared across all instances. Always use `default_factory=list` instead of `[]`.
:::

## `frozen=True` — Immutable Dataclasses

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on frozen true immutable dataclasses](https://realpython.com/search?q=frozen+true+immutable+dataclasses).
:::


Setting `frozen=True` makes instances read-only. Trying to set an attribute raises `FrozenInstanceError`.

```python
>>> @dataclass(frozen=True)
... class ImmutablePoint:
...     x: float
...     y: float
...
>>> p = ImmutablePoint(1.0, 2.0)
>>> p.x = 3.0
Traceback (most recent call last):
    ...
dataclasses.FrozenInstanceError: cannot assign to field 'x'
```

## `order=True` — Comparison Methods

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on order true comparison methods](https://realpython.com/search?q=order+true+comparison+methods).
:::


Setting `order=True` generates `__lt__`, `__le__`, `__gt__`, `__ge__` based on field order.

```python
>>> @dataclass(order=True)
... class Person:
...     name: str
...     age: int
...
>>> alice = Person("Alice", 30)
>>> bob = Person("Bob", 25)
>>> alice > bob  # compares name first, then age
False
```

## `__post_init__` — Post-Initialization Hook

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on __post_init__ post-initialization hook](https://realpython.com/search?q=__post_init__+post-initialization+hook).
:::


`__post_init__` is called after `__init__` completes. Use it for validation, derived fields, or normalizing values.

```python
>>> from dataclasses import dataclass, field

>>> @dataclass
... class Rectangle:
...     width: float
...     height: float
...     area: float = field(init=False)
...
...     def __post_init__(self):
...         if self.width <= 0 or self.height <= 0:
...             raise ValueError("Dimensions must be positive")
...         self.area = self.width * self.height
...
>>> r = Rectangle(3.0, 4.0)
>>> r.area
12.0
```

## `InitVar` — Fields for Initialization Only

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on initvar fields for initialization only](https://realpython.com/search?q=initvar+fields+for+initialization+only).
:::


`InitVar` declares fields that are passed to `__init__` and `__post_init__` but are not stored as instance attributes.

```python
>>> from dataclasses import dataclass, field, InitVar

>>> @dataclass
... class DatabaseConnection:
...     host: str
...     port: int = 5432
...     timeout: InitVar[float] = 30.0
...     _conn: object = field(init=False, repr=False)
...
...     def __post_init__(self, timeout):
...         print(f"Connecting with timeout={timeout}s")
...         self._conn = f"connected to {self.host}:{self.port}"
...
>>> db = DatabaseConnection("localhost")
Connecting with timeout=30.0s
>>> db.host
'localhost'
```

## Inheritance with Dataclasses

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on inheritance with dataclasses](https://realpython.com/search?q=inheritance+with+dataclasses).
:::


Dataclasses support inheritance. Fields from parent classes appear first in the child's `__init__`.

```python
>>> @dataclass
... class Base:
...     x: int = 0
...
>>> @dataclass
... class Derived(Base):
...     y: int = 0
...
>>> d = Derived(x=1, y=2)
>>> d
Derived(x=1, y=2)
```

::: warning
When using inheritance, fields in a child class with defaults must come after parent fields without defaults. Use `field(default=...)` carefully to avoid the "non-default argument follows default argument" error in generated `__init__`.
:::

## Conversion Functions: `asdict`, `astuple`, `replace`

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on conversion functions asdict astuple replace](https://realpython.com/search?q=conversion+functions+asdict+astuple+replace).
:::


These utility functions convert dataclasses to dictionaries, tuples, or create modified copies.

```python
>>> from dataclasses import dataclass, asdict, astuple, replace

>>> @dataclass
... class Address:
...     street: str
...     city: str
...
>>> @dataclass
... class Employee:
...     name: str
...     address: Address
...
>>> e = Employee("Alice", Address("123 Main", "NYC"))
>>> asdict(e)
{'name': 'Alice', 'address': {'street': '123 Main', 'city': 'NYC'}}
>>> astuple(e)
('Alice', ('123 Main', 'NYC'))

# replace — create shallow copy with some fields changed
>>> e2 = replace(e, name="Bob")
>>> e2
Employee(name='Bob', address=Address(street='123 Main', city='NYC'))
```

## `slots=True` — Memory Optimization (Python 3.10+)

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on slots true memory optimization python 3 10](https://realpython.com/search?q=slots+true+memory+optimization+python+3+10).
:::


Setting `slots=True` generates `__slots__` for the class, reducing memory overhead — especially valuable when creating many instances.

```python
>>> @dataclass(slots=True)
... class LightweightPoint:
...     x: float
...     y: float
...
>>> p = LightweightPoint(1.0, 2.0)
>>> p.z = 3.0  # slots prevent adding new attributes
Traceback (most recent call last):
    ...
AttributeError: 'LightweightPoint' object has no attribute 'z'
```

## Comparison: Dataclasses vs namedtuple vs TypedDict

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on comparison dataclasses vs namedtuple vs typeddict](https://realpython.com/search?q=comparison+dataclasses+vs+namedtuple+vs+typeddict).
:::


```python
>>> from dataclasses import dataclass
>>> from collections import namedtuple
>>> from typing import TypedDict

# namedtuple — immutable, compact, no type hints at runtime
>>> PointNT = namedtuple("PointNT", ["x", "y"])
>>> p1 = PointNT(1, 2)

# dataclass — mutable by default, full type annotations, flexible
>>> @dataclass
... class PointDC:
...     x: int
...     y: int
...
>>> p2 = PointDC(1, 2)

# TypedDict — dict-like, type hints only for static checkers
>>> class PointTD(TypedDict):
...     x: int
...     y: int
...
>>> p3: PointTD = {"x": 1, "y": 2}
```

Dataclasses are the most flexible choice for new code when you need mutable data with type annotations. Use `namedtuple` for immutable lightweight containers, and `TypedDict` when you must use dicts (e.g., JSON serialization).
