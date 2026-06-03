---
title: NumPy
---

# NumPy

[[toc]]
NumPy is the fundamental package for scientific computing in Python. It provides a high-performance multidimensional array object and tools for working with these arrays. Understanding NumPy's array operations, broadcasting rules, and linear algebra routines is essential for any data science or numerical computing workflow.

## Array Creation

Create arrays from Python lists or use specialized constructors for common patterns.

```python
>>> import numpy as np

# From lists
>>> a = np.array([1, 2, 3, 4, 5])
>>> b = np.array([[1, 2], [3, 4]])

# Filled arrays
>>> np.zeros((2, 3))
array([[0., 0., 0.],
       [0., 0., 0.]])

>>> np.ones((2, 3))
array([[1., 1., 1.],
       [1., 1., 1.]])

>>> np.eye(3)           # Identity matrix
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])

# Sequence arrays
>>> np.arange(0, 10, 2)   # Start, stop, step
array([0, 2, 4, 6, 8])

>>> np.linspace(0, 1, 5)  # 5 evenly spaced points
array([0.  , 0.25, 0.5 , 0.75, 1.  ])

# Random arrays
>>> np.random.rand(2, 3)    # Uniform [0, 1)
>>> np.random.randn(2, 3)   # Standard normal
>>> np.random.randint(0, 10, size=(2, 3))
>>> np.random.seed(42)      # Reproducibility
```

## Shape Manipulation

Reshape, flatten, and rearrange array dimensions without copying data when possible.

```python
>>> a = np.arange(12)

>>> a.reshape(3, 4)        # Returns a view when possible
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])

>>> a.ravel()              # Flatten to 1D (returns view if contiguous)
>>> a.flatten()            # Always returns a copy

>>> np.expand_dims(a, axis=0).shape  # Add dimension
(1, 12)

>>> a = np.array([[1, 2, 3], [4, 5, 6]])
>>> np.squeeze(a).shape    # Remove length-1 dimensions
(2, 3)

>>> a.T                    # Transpose
array([[1, 4],
       [2, 5],
       [3, 6]])

>>> a.transpose(1, 0)      # Explicit axis permutation
array([[1, 4],
       [2, 5],
       [3, 6]])

>>> a = a.reshape(3, 4)
>>> a.reshape(-1)          # Auto-infer dimension
```

::: warning
`reshape` on non-contiguous arrays may return a copy; use `np.ascontiguousarray(a)` first if you need a view.
:::

## Indexing and Slicing

NumPy supports powerful indexing including slicing, fancy indexing, and boolean masking.

```python
>>> a = np.arange(12).reshape(3, 4)
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])

# Basic slicing
>>> a[1, 2]          # Single element: 6
>>> a[0]             # First row
>>> a[:, 1]          # Second column
>>> a[0:2, 1:3]      # Submatrix

# Fancy indexing with integer arrays
>>> a[[0, 2], [1, 3]]    # (0,1) and (2,3): array([1, 11])
>>> a[[0, 2]]            # Rows 0 and 2
>>> a[:, [1, 3]]         # Columns 1 and 3

# Boolean masking
>>> mask = a > 5
>>> a[mask]
array([ 6,  7,  8,  9, 10, 11])

>>> a[a % 2 == 0] = -1   # Set even elements to -1
```

## Broadcasting

Broadcasting allows arithmetic between arrays of different shapes by automatically expanding dimensions.

```python
>>> a = np.array([[1, 2, 3], [4, 5, 6]])   # (2, 3)
>>> b = np.array([10, 20, 30])              # (3,) → broadcasts to (1, 3) → (2, 3)

>>> a + b
array([[11, 22, 33],
       [14, 25, 36]])

>>> a * np.array([[10], [20]])  # (2, 3) * (2, 1) → (2, 3)
array([[10, 40, 90],
       [80, 100, 120]])

# Broadcasting rules: trailing dimensions must match or be 1/missing
>>> x = np.ones((3, 1, 5))
>>> y = np.ones((1, 4, 1))
>>> (x + y).shape           # (3, 4, 5)
```

::: warning
Broadcasting can create large intermediate arrays in memory. Be mindful when working with very high-dimensional data.
:::

## Universal Functions (ufunc)

Element-wise operations optimized in C. Most math operations are ufuncs.

```python
>>> a = np.array([1, 2, 3, 4])

# Arithmetic ufuncs
>>> np.add(a, 10)
>>> np.subtract(a, 2)
>>> np.multiply(a, 2)
>>> np.divide(a, 3)
>>> np.power(a, 2)

# Trigonometric
>>> np.sin(a), np.cos(a), np.tan(a)

# Exponential and logarithmic
>>> np.exp(a), np.log(a), np.log10(a), np.log2(a)

# Rounding
>>> np.round(np.array([1.234, 5.678]), 1)
array([1.2, 5.7])

# Comparison
>>> np.greater(a, 2)
>>> np.where(a > 2, a, 0)    # Condition, x, y

# Clip
>>> np.clip(a, 1, 3)
array([1, 2, 3, 3])
```

## Aggregation

Compute summary statistics across entire arrays or along specific axes.

```python
>>> a = np.array([[1, 2, 3], [4, 5, 6]])

>>> a.sum()          # 21
>>> a.sum(axis=0)    # Column sums: array([5, 7, 9])
>>> a.sum(axis=1)    # Row sums: array([6, 15])

>>> a.mean()         # 3.5
>>> a.mean(axis=0)   # array([2.5, 3.5, 4.5])

>>> a.std()          # Standard deviation
>>> a.min()          # 1
>>> a.max()          # 6
>>> a.argmin()       # Index of min: 0
>>> a.argmax()       # Index of max: 5

>>> np.median(a)
>>> np.percentile(a, [25, 50, 75])
>>> np.cumsum(a)     # Cumulative sum

# Axis-specific argmin/argmax
>>> a.argmax(axis=0)  # array([1, 1, 1])
```

## Linear Algebra

NumPy's `linalg` submodule provides common linear algebra operations.

```python
>>> A = np.array([[1, 2], [3, 4]])
>>> b = np.array([5, 6])

# Dot product (preferred over a.dot(b))
>>> np.dot(A, b)
array([17, 39])

# Matrix multiplication (Python 3.5+)
>>> A @ b
array([17, 39])

>>> np.matmul(A, np.array([[2], [3]]))
array([[ 8],
       [18]])

# Matrix inverse
>>> np.linalg.inv(A)
array([[-2. ,  1. ],
       [ 1.5, -0.5]])

# Solve linear system Ax = b
>>> np.linalg.solve(A, b)
array([-4.,  4.5])

# Eigenvalues and eigenvectors
>>> vals, vecs = np.linalg.eig(A)
>>> vals
array([-0.37228132,  5.37228132])

# Singular value decomposition
>>> U, S, Vt = np.linalg.svd(A)

# Norms
>>> np.linalg.norm(A)          # Frobenius norm
>>> np.linalg.norm(A, ord=2)   # Spectral norm

# Determinant and trace
>>> np.linalg.det(A)
>>> np.trace(A)

# Outer and inner products
>>> np.outer(np.array([1, 2]), np.array([3, 4]))
array([[3, 4],
       [6, 8]])
```

## Saving and Loading

Persist numpy arrays to disk in binary or text formats.

```python
>>> a = np.array([1, 2, 3, 4, 5])

# Single array — binary .npy format
>>> np.save('array.npy', a)
>>> loaded = np.load('array.npy')

# Multiple arrays — compressed .npz archive
>>> b = np.array([10, 20])
>>> np.savez('arrays.npz', x=a, y=b)
>>> data = np.load('arrays.npz')
>>> data['x'], data['y']

# Compressed archive (smaller file size)
>>> np.savez_compressed('arrays.npz', x=a, y=b)

# Text format — human readable
>>> np.savetxt('array.csv', a, delimiter=',')
>>> loaded = np.loadtxt('array.csv', delimiter=',')

# Structured text with header
>>> np.savetxt('array.csv', a, delimiter=',', header='values', comments='')
```

## Set Operations

Treat 1D arrays as sets for common set operations.

```python
>>> a = np.array([1, 2, 3, 4])
>>> b = np.array([3, 4, 5, 6])

>>> np.intersect1d(a, b)
array([3, 4])
>>> np.union1d(a, b)
array([1, 2, 3, 4, 5, 6])
>>> np.setdiff1d(a, b)
array([1, 2])
>>> np.setxor1d(a, b)
array([1, 2, 5, 6])
>>> np.in1d(a, b)
array([False, False,  True,  True])
```

## References

- [NumPy Documentation](https://numpy.org/doc/stable/)
- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy Linear Algebra](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [NumPy IO Routines](https://numpy.org/doc/stable/reference/routines.io.html)
