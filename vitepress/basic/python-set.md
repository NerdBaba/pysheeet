---
title: Set
---

# Set

[[toc]]
Sets are unordered collections of unique elements in Python. They provide O(1) average time complexity for membership testing and support mathematical set operations like union, intersection, and difference. This cheat sheet covers set comprehensions, common set operations, uniquifying lists, and the immutable frozenset type.

The source code is available on [GitHub](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/set.py).

## References

- [Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)

## Create a Set

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on create a set](https://realpython.com/search?q=create+a+set).
:::


Create sets using curly braces `{}` or the `set()` constructor. Note that empty curly braces `{}` create a dict, not a set.

```python
>>> s = {1, 2, 3}
>>> s
{1, 2, 3}
>>> s = set([1, 2, 2, 3])
>>> s
{1, 2, 3}
>>> empty = set()  # not {}
>>> type(empty)
<class 'set'>
```

## Create Sets with Set Comprehension

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on create sets with set comprehension](https://realpython.com/search?q=create+sets+with+set+comprehension).
:::


Like list comprehensions, set comprehensions provide a concise way to create sets. The syntax uses curly braces `{}` instead of square brackets.

```python
>>> a = [1, 2, 5, 6, 6, 6, 7]
>>> s = {x for x in a}
>>> s
{1, 2, 5, 6, 7}
>>> s = {x for x in a if x > 3}
>>> s
{5, 6, 7}
>>> s = {x ** 2 for x in range(5)}
>>> s
{0, 1, 4, 9, 16}
```

## Remove Duplicates from a List

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on remove duplicates from a list](https://realpython.com/search?q=remove+duplicates+from+a+list).
:::


Converting a list to a set automatically removes duplicate elements. This is one of the most common use cases for sets.

```python
>>> a = [1, 2, 2, 2, 3, 4, 5, 5]
>>> list(set(a))
[1, 2, 3, 4, 5]
```

To preserve the original order, use `dict.fromkeys()` (Python 3.7+):

```python
>>> a = [3, 1, 2, 1, 3, 2]
>>> list(dict.fromkeys(a))
[3, 1, 2]
```

## Add Items to a Set

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on add items to a set](https://realpython.com/search?q=add+items+to+a+set).
:::


Use `add()` to add a single element, or `update()` to add multiple elements.

```python
>>> s = {1, 2, 3}
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.update([5, 6, 7])
>>> s
{1, 2, 3, 4, 5, 6, 7}
>>> s |= {8, 9}  # same as update
>>> s
{1, 2, 3, 4, 5, 6, 7, 8, 9}
```

## Remove Items from a Set

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on remove items from a set](https://realpython.com/search?q=remove+items+from+a+set).
:::


Use `remove()` to remove an element (raises KeyError if not found), or `discard()` to remove without error. Use `pop()` to remove an arbitrary element.

```python
>>> s = {1, 2, 3, 4, 5}
>>> s.remove(3)
>>> s
{1, 2, 4, 5}
>>> s.discard(10)  # no error if not found
>>> s.pop()  # remove arbitrary element
1
>>> s.clear()  # remove all
>>> s
set()
```

## Union with `|` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on union with operator](https://realpython.com/search?q=union+with+operator).
:::


The union of two sets contains all elements from both sets. Use the `|` operator or the `union()` method.

```python
>>> a = {1, 2, 3}
>>> b = {3, 4, 5}
>>> a | b
{1, 2, 3, 4, 5}
>>> a.union(b)
{1, 2, 3, 4, 5}
>>> a | b | {6, 7}  # multiple sets
{1, 2, 3, 4, 5, 6, 7}
```

## Intersection with `&` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on intersection with operator](https://realpython.com/search?q=intersection+with+operator).
:::


The intersection of two sets contains only elements that exist in both sets. Use the `&` operator or the `intersection()` method.

```python
>>> a = {1, 2, 3, 4}
>>> b = {3, 4, 5, 6}
>>> a & b
{3, 4}
>>> a.intersection(b)
{3, 4}
```

## Find Common Elements Between Lists

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on find common elements between lists](https://realpython.com/search?q=find+common+elements+between+lists).
:::


Finding common items between two lists is a practical application of set intersection.

```python
>>> a = [1, 1, 2, 3]
>>> b = [3, 5, 5, 6]
>>> list(set(a) & set(b))
[3]
```

## Difference with `-` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on difference with - operator](https://realpython.com/search?q=difference+with+-+operator).
:::


The difference of two sets contains elements that are in the first set but not in the second. Use the `-` operator or the `difference()` method.

```python
>>> a = {1, 2, 3, 4}
>>> b = {3, 4, 5, 6}
>>> a - b
{1, 2}
>>> b - a
{5, 6}
```

## Symmetric Difference with `^` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on symmetric difference with operator](https://realpython.com/search?q=symmetric+difference+with+operator).
:::


The symmetric difference contains elements that are in either set, but not in both. Use the `^` operator or the `symmetric_difference()` method.

```python
>>> a = {1, 2, 3}
>>> b = {3, 4, 5}
>>> a ^ b
{1, 2, 4, 5}
```

## Check Subset with `<=` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on check subset with operator](https://realpython.com/search?q=check+subset+with+operator).
:::


Use `<=` or `issubset()` to check if all elements of one set are in another. Use `<` for proper subset (subset but not equal).

```python
>>> a = {1, 2}
>>> b = {1, 2, 3, 4}
>>> a <= b  # a is subset of b
True
>>> a < b   # a is proper subset
True
>>> a <= a  # equal sets
True
>>> a < a   # not proper subset
False
```

## Check Superset with `>=` Operator

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on check superset with operator](https://realpython.com/search?q=check+superset+with+operator).
:::


Use `>=` or `issuperset()` to check if a set contains all elements of another.

```python
>>> a = {1, 2, 3, 4}
>>> b = {1, 2}
>>> a >= b  # a is superset of b
True
>>> a > b   # a is proper superset
True
```

## Check Disjoint Sets

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on check disjoint sets](https://realpython.com/search?q=check+disjoint+sets).
:::


Two sets are disjoint if they have no elements in common. Use `isdisjoint()` to check.

```python
>>> a = {1, 2, 3}
>>> b = {4, 5, 6}
>>> a.isdisjoint(b)
True
>>> c = {3, 4, 5}
>>> a.isdisjoint(c)
False
```

## Membership Testing

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on membership testing](https://realpython.com/search?q=membership+testing).
:::


Sets provide O(1) average time complexity for membership testing, making them much faster than lists for this operation.

```python
>>> s = {1, 2, 3, 4, 5}
>>> 3 in s
True
>>> 10 in s
False
>>> 10 not in s
True
```

## Frozenset - Immutable Set

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on frozenset - immutable set](https://realpython.com/search?q=frozenset+-+immutable+set).
:::


`frozenset` is an immutable version of set. It can be used as a dictionary key or as an element of another set.

```python
>>> fs = frozenset([1, 2, 3])
>>> fs
frozenset({1, 2, 3})
>>> fs.add(4)  # raises AttributeError
AttributeError: 'frozenset' object has no attribute 'add'
```

Use frozenset as dictionary key:

```python
>>> d = {frozenset([1, 2]): "a", frozenset([3, 4]): "b"}
>>> d[frozenset([1, 2])]
'a'
```

Use frozenset in a set:

```python
>>> s = {frozenset([1, 2]), frozenset([3, 4])}
>>> frozenset([1, 2]) in s
True
```

## Set Operations Summary

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on set operations summary](https://realpython.com/search?q=set+operations+summary).
:::


```python
# Creation
s = {1, 2, 3}           # literal
s = set([1, 2, 3])      # from iterable
s = {x for x in range(5)}  # comprehension

# Add/Remove
s.add(x)                # add single element
s.update([x, y])        # add multiple elements
s.remove(x)             # remove (KeyError if missing)
s.discard(x)            # remove (no error if missing)
s.pop()                 # remove arbitrary element
s.clear()               # remove all

# Set Operations
a | b                   # union
a & b                   # intersection
a - b                   # difference
a ^ b                   # symmetric difference

# Comparisons
a <= b                  # subset
a < b                   # proper subset
a >= b                  # superset
a > b                   # proper superset
a.isdisjoint(b)         # no common elements

# Membership
x in s                  # O(1) lookup
x not in s
```
