---
title: Argparse
---

# Argparse

Source  
[src/basic/argparse\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/argparse_.py)

[[toc]]

Python's `argparse` module parses command-line arguments and options with automatic help generation. It supports positional arguments, optional flags, type validation, subcommands, and mutually exclusive options — everything needed for robust CLI tools. Argparse is part of the standard library, so it's always available with no extra dependencies.

## Basic ArgumentParser

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic argumentparser](https://realpython.com/search?q=basic+argumentparser).
:::

Create a parser, add arguments, and parse. The `--help` flag is generated automatically.

```python
import argparse

parser = argparse.ArgumentParser(
    prog="myapp",
    description="A sample CLI tool",
    epilog="For more info visit https://example.com",
)

parser.add_argument("filename", help="File to process")       # positional
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("--output", "-o", default="out.txt", help="Output file")

args = parser.parse_args()

print(args.filename)   # positional argument
print(args.verbose)    # True/False
print(args.output)     # 'out.txt' by default
```

## Positional Arguments

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on positional arguments](https://realpython.com/search?q=positional+arguments).
:::

Positional arguments are required by default and don't use `--` prefixes. They're accessed by the name you give them (dest).

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file path")
parser.add_argument("output", help="Output file path")
parser.add_argument("mode", choices=["encode", "decode"], help="Operation mode")

args = parser.parse_args()
print(args.input, args.output, args.mode)
```

## Optional Arguments

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on optional arguments](https://realpython.com/search?q=optional+arguments).
:::

Optional arguments start with `--` or `-`. They can be flags (no value) or accept values.

```python
import argparse

parser = argparse.ArgumentParser()

# Boolean flag
parser.add_argument("--verbose", action="store_true", help="Verbose output")
parser.add_argument("--quiet", action="store_true", help="Suppress output")

# Short and long forms
parser.add_argument("-c", "--config", default="config.yaml", help="Config file")
parser.add_argument("-n", "--count", type=int, default=1, help="Number of times")

args = parser.parse_args()
```

## Type Conversion

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on type conversion](https://realpython.com/search?q=type+conversion).
:::

Use `type` to automatically convert string arguments to the desired type. The parser validates and converts before returning.

```python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--count", type=int, default=1)
parser.add_argument("--ratio", type=float, default=0.5)
parser.add_argument("--names", type=str, nargs="+")  # one or more strings

# Custom type conversion
def valid_port(value):
    port = int(value)
    if not 0 < port <= 65535:
        raise argparse.ArgumentTypeError(f"Invalid port: {port}")
    return port

parser.add_argument("--port", type=valid_port, required=True)

args = parser.parse_args()
```

## Choices

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on choices](https://realpython.com/search?q=choices).
:::

Restrict an argument's value to a fixed set of options. Argparse generates an error message listing valid choices.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["upload", "download", "sync"], required=True)
parser.add_argument("--format", choices=["json", "yaml", "toml"], default="json")

# With integers
parser.add_argument("--level", type=int, choices=[1, 2, 3], default=2)

args = parser.parse_args()
```

## nargs — Multiple Values

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on nargs multiple values](https://realpython.com/search?q=nargs+multiple+values).
:::

Control how many values an argument consumes. `nargs` takes an integer, `'?'`, `'*'`, `'+'`, or `argparse.REMAINDER`.

```python
import argparse

parser = argparse.ArgumentParser()

# Exactly 2 values
parser.add_argument("--pair", nargs=2, type=float, help="x y coordinates")

# 0 or 1 value (optional value)
parser.add_argument("--output", nargs="?", const="default.txt", help="Output file")

# 0 or more values
parser.add_argument("files", nargs="*", help="Zero or more files")

# 1 or more values
parser.add_argument("inputs", nargs="+", help="One or more inputs")

# All remaining arguments (for wrapping another command)
parser.add_argument("rest", nargs=argparse.REMAINDER)

args = parser.parse_args()
```

## action='store_true' / 'store_false'

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on action store_true store_false](https://realpython.com/search?q=action+store_true+store_false).
:::

Convenience flags that set a boolean. `store_true` sets the attribute to `True` when the flag is present, `store_false` sets it to `False`. Both default to the opposite value when absent.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="Enable verbose")
parser.add_argument("--no-color", action="store_true", help="Disable colors")
parser.add_argument("--preserve", action="store_false", dest="overwrite", help="Don't overwrite")

args = parser.parse_args()
# --verbose  → args.verbose = True
# absent     → args.verbose = False
# --preserve → args.overwrite = False
```

## Default Values

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on default values](https://realpython.com/search?q=default+values).
:::

Every argument can have a default value. Argparse supports two special constants: `SUPPRESS` omits the attribute entirely if not provided, and `PARSER` is used internally for subparsers.

```python
import argparse

parser = argparse.ArgumentParser()

# Basic default
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", type=int, default=8080)

# Default from environment variable
import os
parser.add_argument("--api-key", default=os.environ.get("API_KEY", ""))

# SUPPLESS — don't add attribute if argument not provided
parser.add_argument("--optional", nargs="?", default=argparse.SUPPRESS)

args = parser.parse_args()
print(getattr(args, "optional", "not provided"))
```

## Mutually Exclusive Groups

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on mutually exclusive groups](https://realpython.com/search?q=mutually+exclusive+groups).
:::

Define options that cannot be used together. Argparse generates an automatic error message if the user provides conflicting flags.

```python
import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--start", action="store_true", help="Start service")
group.add_argument("--stop", action="store_true", help="Stop service")
group.add_argument("--restart", action="store_true", help="Restart service")

# Another exclusive group (not required)
output = parser.add_mutually_exclusive_group()
output.add_argument("--json", action="store_true", help="JSON output")
output.add_argument("--yaml", action="store_true", help="YAML output")

args = parser.parse_args()
```

## Argument Groups

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on argument groups](https://realpython.com/search?q=argument+groups).
:::

Organize help output into logical sections for better user experience.

```python
import argparse

parser = argparse.ArgumentParser(description="Data processing tool")

# Positional (shown separately by default)
parser.add_argument("input", help="Input file")

# Optional group header
net_group = parser.add_argument_group("Network Options")
net_group.add_argument("--host", default="localhost")
net_group.add_argument("--port", type=int, default=8080)
net_group.add_argument("--tls", action="store_true")

# Advanced group
adv_group = parser.add_argument_group("Advanced Options")
adv_group.add_argument("--timeout", type=int, default=30)
adv_group.add_argument("--retries", type=int, default=3)

args = parser.parse_args()
```

## Subparsers — Subcommands

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on subparsers subcommands](https://realpython.com/search?q=subparsers+subcommands).
:::

Create nested commands like `git commit`, `git push`. Each subcommand gets its own set of arguments.

```python
import argparse

parser = argparse.ArgumentParser(description="CLI with subcommands")
subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

# init subcommand
init_parser = subparsers.add_parser("init", help="Initialize repo")
init_parser.add_argument("path", nargs="?", default=".", help="Path to init")

# clone subcommand
clone_parser = subparsers.add_parser("clone", help="Clone repo")
clone_parser.add_argument("url", help="Repository URL")
clone_parser.add_argument("--depth", type=int, help="Shallow clone depth")

# commit subcommand
commit_parser = subparsers.add_parser("commit", help="Commit changes")
commit_parser.add_argument("-m", "--message", required=True, help="Commit message")
commit_parser.add_argument("--amend", action="store_true", help="Amend previous commit")

args = parser.parse_args()

if args.command == "init":
    print(f"Init at {args.path}")
elif args.command == "clone":
    print(f"Clone {args.url} (depth={args.depth})")
elif args.command == "commit":
    print(f"Commit: {args.message}")
```

## parse_known_args

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on parse_known_args](https://realpython.com/search?q=parse_known_args).
:::

Parse only recognized arguments and return the rest in a list. Useful for wrapping other commands or skipping arguments for another parser.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--config", default="config.yaml")

# Parse only known args; collect unknown in second element
args, unknown = parser.parse_known_args()

print(f"Known: {args}")
print(f"Unknown: {unknown}")

# Pass unknown args to another command
import subprocess
subprocess.run(["docker"] + unknown)
```

## Error Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on error handling](https://realpython.com/search?q=error+handling).
:::

Override default error behavior to suppress exit on errors, especially useful in test environments or interactive shells.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)

# Parse without sys.exit on error
try:
    args = parser.parse_args(["--unknown"])
except SystemExit as e:
    print(f"Caught exit: {e.code}")

# Custom error handler
class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

custom_parser = CustomParser()
custom_parser.add_argument("--port", type=int)

try:
    args = custom_parser.parse_args(["--port", "bad"])
except ValueError as e:
    print(f"Parse error: {e}")
```

## References

- [argparse — Parser for command-line options, arguments and subcommands](https://docs.python.org/3/library/argparse.html)
- [Argparse Tutorial](https://docs.python.org/3/howto/argparse.html)
