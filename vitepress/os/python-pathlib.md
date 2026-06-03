---
title: Pathlib
---

# Pathlib

Source  
[src/basic/pathlib\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/pathlib_.py)

[[toc]]

Python's `pathlib` module (Python 3.4+) provides an object-oriented interface to filesystem paths, replacing the older `os.path` string-based approach. `Path` objects handle platform differences automatically (forward slashes on Unix, backslashes on Windows) and expose methods for common operations like reading, writing, globbing, and directory traversal. The `/` operator joins path components intuitively. For most filesystem tasks in modern Python, `pathlib` is the recommended choice.

## Creating Path Objects

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on creating path objects](https://realpython.com/search?q=creating+path+objects).
:::

`Path()` accepts a string path or multiple path components. The `/` operator joins paths, and class methods provide well-known directory shortcuts.

```python
from pathlib import Path

# Construction from string
p = Path("/usr/local/bin/python3")
p = Path("relative/path/to/file.txt")

# Join paths with / operator
config = Path.home() / ".config" / "app" / "config.json"

# Current directory and home
cwd = Path.cwd()       # Path('/home/user/project')
home = Path.home()     # Path('/home/user')

# Resolve relative paths
abs_path = Path(".").resolve()  # Path('/home/user/project')
```

::: warning
The `/` operator only works when the left operand is a `Path` object. `Path.home() + "/subdir"` will fail — use the `/` operator consistently.
:::

## Path Properties

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on path properties](https://realpython.com/search?q=path+properties).
:::

Access components of a path without string parsing. These properties never raise exceptions — they simply extract information from the path string.

```python
p = Path("/home/user/documents/report.pdf")

p.name      # 'report.pdf'   — final component
p.stem      # 'report'       — name without suffix
p.suffix    # '.pdf'         — file extension with dot
p.parent    # Path('/home/user/documents')
p.anchor    # '/'            — root of the filesystem

# Multiple suffixes
p2 = Path("archive.tar.gz")
p2.suffix   # '.gz'
p2.suffixes # ['.tar', '.gz']

# Walk up directories
p.parents[0]   # Path('/home/user/documents')
p.parents[1]   # Path('/home/user')
p.parents[2]   # Path('/home')
p.parents[3]   # Path('/')

# Parts as tuple
p.parts     # ('/', 'home', 'user', 'documents', 'report.pdf')
```

## Checking Existence and Type

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on checking existence and type](https://realpython.com/search?q=checking+existence+and+type).
:::

Test whether a path exists and what kind of filesystem entry it is. These are non-raising checks — they return `True`/`False` instead of throwing exceptions.

```python
p = Path("some_file.txt")

p.exists()      # True/False — path exists
p.is_file()     # True if regular file (not dir, not symlink)
p.is_dir()      # True if directory
p.is_symlink()  # True if symbolic link
p.is_absolute() # True if absolute path
p.is_mount()    # True if mount point (Unix)
```

## Reading and Writing Files

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on reading and writing files](https://realpython.com/search?q=reading+and+writing+files).
:::

`Path` objects provide one-liner methods for common file I/O, avoiding the `open()` context manager for simple cases.

```python
p = Path("hello.txt")

# Text I/O
p.write_text("Hello, World!", encoding="utf-8")
content = p.read_text(encoding="utf-8")

# Binary I/O
p.write_bytes(b"\x00\x01\x02")
data = p.read_bytes()

# With open() for more control
with p.open("a", encoding="utf-8") as f:
    f.write("appended line\n")
```

::: warning
`write_text()` and `write_bytes()` overwrite the file without warning. Use `p.open("x")` for exclusive creation that fails if the file exists.
:::

## Directory Operations

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on directory operations](https://realpython.com/search?q=directory+operations).
:::

Create, list, and remove directories. The `parents=True` option mirrors `mkdir -p` behavior.

```python
p = Path("new_dir")

# Create directory
p.mkdir()                           # Fails if exists or parent missing
p.mkdir(parents=True, exist_ok=True)  # Like mkdir -p

# Remove directory (must be empty)
p.rmdir()

# List directory contents
for child in Path(".").iterdir():
    print(child.name, child.is_dir())

# For non-empty dirs, use shutil.rmtree
import shutil
shutil.rmtree("non_empty_dir")
```

## Renaming, Moving, and Deleting

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on renaming moving and deleting](https://realpython.com/search?q=renaming+moving+and+deleting).
:::

Rename or replace files and delete individual files. `rename()` fails if the target exists on some platforms; `replace()` always overwrites the target atomically.

```python
p = Path("old.txt")

# Rename (same filesystem, may fail if target exists)
p.rename("new.txt")

# Replace (atomic, overwrites destination)
p.replace("dest.txt")

# Delete file
p.unlink()
p.unlink(missing_ok=True)  # No error if file doesn't exist (3.8+)
```

## Glob Patterns

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on glob patterns](https://realpython.com/search?q=glob+patterns).
:::

Search for files matching patterns. `glob()` matches in the current directory, `rglob()` matches recursively. `**` matches any number of subdirectories.

```python
p = Path(".")

# All Python files in current directory
for f in p.glob("*.py"):
    print(f)

# Recursive — all Python files anywhere under p
for f in p.rglob("*.py"):
    print(f)

# Equivalent to rglob
for f in p.glob("**/*.py"):
    print(f)

# Single-character wildcard
for f in p.glob("file?.txt"):
    print(f)  # file1.txt, file2.txt

# Filter directories
for d in p.glob("**/*"):
    if d.is_dir():
        print(d)
```

## File Metadata

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on file metadata](https://realpython.com/search?q=file+metadata).
:::

Retrieve file size, modification times, and other metadata via `stat()`, or use convenience properties.

```python
p = Path("file.txt")
stat = p.stat()

stat.st_size    # File size in bytes
stat.st_mtime   # Last modification timestamp
stat.st_ctime   # Creation time (Unix) or metadata change (Windows)
stat.st_mode    # File permissions as integer

# Convenience — modification time as float
p.stat().st_mtime

# File owner/group (Unix)
stat.st_uid
stat.st_gid
```

## Symlinks

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on symlinks](https://realpython.com/search?q=symlinks).
:::

Create, inspect, and resolve symbolic links.

```python
p = Path("link_to_file")

# Create symlink
p.symlink_to("target_file.txt")
p.symlink_to("/absolute/path", target_is_directory=True)

# Read symlink target
target = p.readlink()  # Path('target_file.txt')

# Check and resolve
p.is_symlink()
real = p.resolve()     # Follow all symlinks to canonical path
```

## Modifying Paths

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on modifying paths](https://realpython.com/search?q=modifying+paths).
:::

Create new `Path` objects with modified components. These methods return new paths without modifying the original — they are pure transformations of the path string.

```python
p = Path("/home/user/docs/report.pdf")

# Change file extension
p.with_suffix(".txt")   # Path('/home/user/docs/report.txt')
p.with_suffix("")       # Path('/home/user/docs/report')

# Change filename
p.with_name("summary.pdf")  # Path('/home/user/docs/summary.pdf')

# Add suffix to path that has none
Path("data").with_suffix(".csv")  # Path('data.csv')
```

## Relative Paths

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on relative paths](https://realpython.com/search?q=relative+paths).
:::

Compute relative paths between two locations or make a path relative to a reference.

```python
p = Path("/home/user/docs/report.pdf")
base = Path("/home/user")

# Relative to another path
rel = p.relative_to(base)   # Path('docs/report.pdf')

# With base comparison (3.12+)
# p.relative_to(base, walk_up=True)  # allows .. components

# Current directory relative to some reference
Path("/home/user/project").relative_to(Path("/home"))  # Path('user/project')
```

## Comparing with os.path

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on comparing with os path](https://realpython.com/search?q=comparing+with+os+path).
:::

The `os.path` module is the older, string-based approach. `pathlib` is preferred for new code.

| Operation | os.path | pathlib |
|---|---|---|
| Join paths | `os.path.join("a", "b")` | `Path("a") / "b"` |
| Split dir/file | `os.path.dirname(p)`, `os.path.basename(p)` | `p.parent`, `p.name` |
| Split extension | `os.path.splitext(p)` | `p.stem`, `p.suffix` |
| Check existence | `os.path.exists(p)` | `Path(p).exists()` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, "w").write(s)` | `Path(p).write_text(s)` |
| List directory | `os.listdir(d)` | `Path(d).iterdir()` |
| Glob | `glob.glob("*.py")` | `Path(".").glob("*.py")` |
| Absolute path | `os.path.abspath(p)` | `Path(p).resolve()` |
| Make dirs | `os.makedirs(p, exist_ok=True)` | `Path(p).mkdir(parents=True, exist_ok=True)` |
| File size | `os.path.getsize(p)` | `Path(p).stat().st_size` |

```python
# os.path (old style)
import os
path = os.path.join("home", "user", "file.txt")
exists = os.path.exists(path)
content = open(path).read()

# pathlib (modern style)
from pathlib import Path
path = Path.home() / "file.txt"
exists = path.exists()
content = path.read_text()
```

## References

- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
- [PEP 428 — The pathlib module](https://peps.python.org/pep-0428/)
- [os.path — Common pathname manipulations](https://docs.python.org/3/library/os.path.html)
