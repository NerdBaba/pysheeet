---
title: ctypes
---

# ctypes

Source  
[src/basic/cext\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/cext_.py)

[[toc]]
ctypes is Python's built-in foreign function interface (FFI) library that allows calling functions in shared libraries (.so on Linux, .dylib on macOS, .dll on Windows) without writing any C code or compiling extensions. It's ideal for quick prototyping, accessing system libraries, or wrapping existing C libraries when you don't want a compilation step. However, ctypes requires manual type declarations and careful memory management, making it more error-prone than alternatives like cffi or pybind11 for complex use cases.

## Loading Shared Libraries

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on loading shared libraries](https://realpython.com/search?q=loading+shared+libraries).
:::

ctypes provides platform-specific loaders for shared libraries. Use `CDLL` for standard C calling convention or `WinDLL` on Windows for stdcall convention. The library search follows system conventions: `LD_LIBRARY_PATH` on Linux, `DYLD_LIBRARY_PATH` on macOS, and `PATH` on Windows.

```python
import platform
from ctypes import CDLL

# Load platform-specific C library
if platform.system() == "Darwin":
    libc = CDLL("libc.dylib")
elif platform.system() == "Linux":
    libc = CDLL("libc.so.6")
else:
    from ctypes import windll
    libc = windll.msvcrt

# Call printf
libc.printf(b"Hello from C: %d\n", 42)
```

## Loading Custom Libraries

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on loading custom libraries](https://realpython.com/search?q=loading+custom+libraries).
:::

For your own compiled C libraries, provide the full path or ensure the library is in the system's library search path. The `use_errno=True` parameter enables proper errno handling for error detection.

```python
from ctypes import CDLL
from ctypes.util import find_library
import os

# Load from current directory
lib_path = os.path.join(os.path.dirname(__file__), "libfoo.so")
lib = CDLL(lib_path, use_errno=True)

# Or use find_library for system libraries
libm_path = find_library("m")  # finds libm.so or libm.dylib
if libm_path:
    libm = CDLL(libm_path)
```

## Basic Type Mapping

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic type mapping](https://realpython.com/search?q=basic+type+mapping).
:::

ctypes provides Python equivalents for C types. Always declare argument types (`argtypes`) and return types (`restype`) explicitly to avoid crashes and ensure correct data conversion. Without these declarations, ctypes assumes all arguments and return values are C `int`.

```python
import platform
from ctypes import CDLL, c_double, c_char_p

if platform.system() == "Darwin":
    libc = CDLL("libc.dylib")
else:
    libc = CDLL("libc.so.6")

# Declare function signature: double atof(const char *)
libc.atof.argtypes = [c_char_p]
libc.atof.restype = c_double

result = libc.atof(b"3.14159")
print(result)  # 3.14159

# Common type mappings:
# c_int      -> int
# c_long     -> long
# c_double   -> double
# c_char_p   -> char* (bytes in Python)
# c_void_p   -> void*
# c_bool     -> _Bool
```

## Calling strlen and abs

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on calling strlen and abs](https://realpython.com/search?q=calling+strlen+and+abs).
:::

Simple examples calling standard C library functions with proper type declarations.

```python
import platform
from ctypes import CDLL, c_char_p, c_size_t

if platform.system() == "Darwin":
    libc = CDLL("libc.dylib")
else:
    libc = CDLL("libc.so.6")

# strlen
libc.strlen.argtypes = [c_char_p]
libc.strlen.restype = c_size_t
assert libc.strlen(b"hello") == 5

# abs (default int types work)
assert libc.abs(-42) == 42
```

## Calling sqrt from libm

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on calling sqrt from libm](https://realpython.com/search?q=calling+sqrt+from+libm).
:::

```python
import platform
from ctypes import CDLL, c_double

if platform.system() == "Darwin":
    libm = CDLL("libm.dylib")
else:
    libm = CDLL("libm.so.6")

libm.sqrt.argtypes = [c_double]
libm.sqrt.restype = c_double

result = libm.sqrt(16.0)
assert abs(result - 4.0) < 1e-10
```

## Calling C Functions

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on calling c functions](https://realpython.com/search?q=calling+c+functions).
:::

This example shows a complete workflow: compile a C library, load it with ctypes, and call functions with proper type declarations. The Fibonacci function demonstrates the performance benefit of C code called from Python.

**C source (fib.c):**

```c
// Compile:
//   Linux: gcc -shared -fPIC -o libfib.so fib.c
//   macOS: clang -shared -fPIC -o libfib.dylib fib.c

unsigned long fib(unsigned long n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
```

**Python usage:**

```python
import platform
from ctypes import CDLL, c_ulong

# Load the library
if platform.system() == "Darwin":
    lib = CDLL("./libfib.dylib")
else:
    lib = CDLL("./libfib.so")

# Declare types
lib.fib.argtypes = [c_ulong]
lib.fib.restype = c_ulong

# Call the function
print(lib.fib(35))  # 9227465
```

**Performance comparison:**

```python
>>> from time import time
>>> def py_fib(n):
...     if n < 2: return n
...     return py_fib(n - 1) + py_fib(n - 2)
...
>>> s = time(); _ = py_fib(35); e = time(); e - s
4.918856859207153
>>> s = time(); _ = lib.fib(35); e = time(); e - s
0.07283687591552734
```

## Pointers and byref

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on pointers and byref](https://realpython.com/search?q=pointers+and+byref).
:::

Use `byref()` to pass arguments by reference (like `&var` in C) and `POINTER()` to create pointer types. `byref()` is more efficient than `pointer()` when you only need to pass a reference to a function.

```python
from ctypes import c_int, byref, pointer, POINTER

# Pointer to integer
value = c_int(42)
ptr = pointer(value)
assert ptr.contents.value == 42

# Modify through pointer
ptr.contents.value = 100
assert value.value == 100

# byref creates a lightweight pointer for passing to C functions
ref = byref(value)

# Create pointer type and array
IntPtr = POINTER(c_int)
arr = (c_int * 3)(1, 2, 3)
```

## Structures

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on structures](https://realpython.com/search?q=structures).
:::

Define C structures by subclassing `Structure` and specifying `_fields_`. Field order must match the C struct exactly. Use `_pack_` to control alignment if needed (e.g., `_pack_ = 1` for packed structs).

```python
import ctypes
import math

class Point(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
    ]

# Create and use
p = Point(3.0, 4.0)
assert p.x == 3.0
assert p.y == 4.0

# Calculate distance
distance = math.sqrt(p.x ** 2 + p.y ** 2)
assert abs(distance - 5.0) < 1e-10
```

## Nested Structures

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on nested structures](https://realpython.com/search?q=nested+structures).
:::

```python
import ctypes

class Point(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
    ]

class Rectangle(ctypes.Structure):
    _fields_ = [
        ("top_left", Point),
        ("bottom_right", Point),
    ]

rect = Rectangle(Point(0, 10), Point(10, 0))
assert rect.top_left.x == 0
assert rect.top_left.y == 10
assert rect.bottom_right.x == 10
```

## Arrays

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on arrays](https://realpython.com/search?q=arrays).
:::

Create C arrays using the multiplication syntax `type * size`. Arrays can be initialized with values and accessed like Python lists. They automatically convert to pointers when passed to C functions.

```python
from ctypes import c_int, c_double, c_char

# Integer array
IntArray5 = c_int * 5
arr = IntArray5(1, 2, 3, 4, 5)
assert arr[0] == 1
assert arr[4] == 5

# Modify elements
arr[0] = 100
assert list(arr) == [100, 2, 3, 4, 5]

# Character array (C string buffer)
buf = (c_char * 256)()
buf.value = b"Hello"
assert buf.value == b"Hello"

# Double array for numerical work
data = (c_double * 3)(1.1, 2.2, 3.3)
assert abs(sum(data) - 6.6) < 1e-10
```

## Array in Structure

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on array in structure](https://realpython.com/search?q=array+in+structure).
:::

Structures can contain fixed-size arrays as members.

```python
import ctypes

class Data(ctypes.Structure):
    _fields_ = [
        ("values", ctypes.c_int * 5),
        ("count", ctypes.c_int)
    ]

d = Data()
d.count = 5
for i in range(5):
    d.values[i] = i * 10

assert list(d.values) == [0, 10, 20, 30, 40]
assert d.count == 5
```

## Using cffi

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on using cffi](https://realpython.com/search?q=using+cffi).
:::

cffi is a cleaner alternative to ctypes with better PyPy compatibility. It uses C-like declarations instead of Python type objects.

```python
import platform
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    int abs(int x);
    size_t strlen(const char *s);
    double sqrt(double x);
""")

if platform.system() == "Darwin":
    libc = ffi.dlopen("libc.dylib")
    libm = ffi.dlopen("libm.dylib")
else:
    libc = ffi.dlopen("libc.so.6")
    libm = ffi.dlopen("libm.so.6")

assert libc.abs(-42) == 42
assert libc.strlen(b"hello") == 5
assert abs(libm.sqrt(16.0) - 4.0) < 1e-10
```

## Error Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on error handling](https://realpython.com/search?q=error+handling).
:::

When calling C functions that set errno on failure, use `use_errno=True` when loading the library and `get_errno()` to retrieve the error code. This is essential for proper error handling with system calls.

```python
import os
import platform
from ctypes import CDLL, get_errno

if platform.system() == "Darwin":
    libc = CDLL("libc.dylib", use_errno=True)
else:
    libc = CDLL("libc.so.6", use_errno=True)

# Try to open a non-existent file
fd = libc.open(b"/nonexistent/path", 0)
if fd == -1:
    errno = get_errno()
    errmsg = f"open failed: {os.strerror(errno)}"
    print(errmsg)  # open failed: No such file or directory
```

## Callbacks

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on callbacks](https://realpython.com/search?q=callbacks).
:::

ctypes can create C-callable function pointers from Python functions using `CFUNCTYPE`. This is useful for C libraries that accept callback functions, such as `qsort()` or event handlers.

```python
import platform
from ctypes import CDLL, CFUNCTYPE, POINTER, c_int, c_void_p, cast, sizeof

if platform.system() == "Darwin":
    libc = CDLL("libc.dylib")
else:
    libc = CDLL("libc.so.6")

# Define callback type: int (*compare)(const void*, const void*)
CMPFUNC = CFUNCTYPE(c_int, c_void_p, c_void_p)

def py_compare(a, b):
    """Compare function for qsort"""
    a_val = cast(a, POINTER(c_int)).contents.value
    b_val = cast(b, POINTER(c_int)).contents.value
    return a_val - b_val

# Create C callback from Python function
c_compare = CMPFUNC(py_compare)

# Use with qsort
arr = (c_int * 5)(5, 2, 8, 1, 9)
libc.qsort(arr, len(arr), sizeof(c_int), c_compare)
print(list(arr))  # [1, 2, 5, 8, 9]
```

## String Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on string handling](https://realpython.com/search?q=string+handling).
:::

C strings require careful handling in ctypes. Use `c_char_p` for immutable strings and `create_string_buffer()` for mutable buffers. Always use bytes (`b"string"`) not str when passing to C functions.

```python
import platform
from ctypes import CDLL, c_char_p, c_int, create_string_buffer

if platform.system() == "Darwin":
    libc = CDLL("libc.dylib")
else:
    libc = CDLL("libc.so.6")

# Immutable string (c_char_p)
libc.puts.argtypes = [c_char_p]
libc.puts(b"Hello, World!")

# Mutable buffer for functions that modify strings
buf = create_string_buffer(100)
libc.strcpy(buf, b"Hello")
libc.strcat(buf, b", World!")
print(buf.value)  # b'Hello, World!'

# Get string length
libc.strlen.argtypes = [c_char_p]
libc.strlen.restype = c_int
print(libc.strlen(b"Hello"))  # 5
```
