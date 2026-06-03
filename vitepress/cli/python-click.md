---
title: Click
---

# Click

Source  
[src/basic/click\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/click_.py)

[[toc]]

Click is a Python package for creating command-line interfaces with minimal boilerplate, using decorators to define commands, options, and arguments. It handles help page generation, input prompting, type conversion, error handling, and nested subcommands automatically. Install with `pip install click`. Compared to `argparse`, Click is more concise and better suited for complex CLI applications with subcommands.

## Basic Command

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic command](https://realpython.com/search?q=basic+command).
:::

Decorators turn functions into CLI commands. The `@click.command()` decorator registers the function, and `@click.option()` adds command-line flags.

```python
import click


@click.command()
@click.option("--name", prompt="Your name", help="The person to greet")
@click.option("--count", default=1, type=int, help="Number of greetings")
def hello(name, count):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    hello()
```

Run with: `python hello.py --name Alice --count 3`

## Options

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on options](https://realpython.com/search?q=options).
:::

Options use `--` prefixes and support short forms, types, defaults, and help text.

```python
import click


@click.command()
@click.option("-n", "--name", type=str, help="Your name")
@click.option("--age", type=int, default=30, help="Your age")
@click.option("--active", is_flag=True, help="Activate feature")
@click.option("--rate", type=float, help="Conversion rate")
@click.option("--colors", multiple=True, help="One or more colors")
def show(name, age, active, rate, colors):
    click.echo(f"Name: {name}, Age: {age}, Active: {active}")
    click.echo(f"Rate: {rate}, Colors: {colors}")


if __name__ == "__main__":
    show()
```

## Arguments

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on arguments](https://realpython.com/search?q=arguments).
:::

Arguments are positional and required unless marked optional. They use `@click.argument()`.

```python
import click


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.argument("format", type=click.Choice(["json", "yaml", "csv"]))
def convert(input_file, output_file, format):
    """Convert INPUT_FILE to OUTPUT_FILE in FORMAT."""
    click.echo(f"Converting {input_file} to {format}")


if __name__ == "__main__":
    convert()
```

Run with: `python convert.py data.csv output.json json`

## Types

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on types](https://realpython.com/search?q=types).
:::

Click provides built-in types beyond basic Python types.

```python
import click


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("--count", type=click.IntRange(1, 100), default=10)
@click.option("--ratio", type=click.FloatRange(0.0, 1.0), default=0.5)
@click.option("--choice", type=click.Choice(["a", "b", "c"]))
@click.option("--email", type=str)
@click.option("--password", hide_input=True, confirmation_prompt=True)
@click.option("--uuid", type=click.UUID)
def process(path, count, ratio, choice, email, password, uuid):
    click.echo(f"Path: {path}, Count: {count}, Ratio: {ratio}")
    click.echo(f"Choice: {choice}, Email: {email}")
    click.echo(f"UUID: {uuid}")
```

## Prompts and Hidden Input

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on prompts and hidden input](https://realpython.com/search?q=prompts+and+hidden+input).
:::

Prompt the user interactively for values. `hide_input` masks typed input, `confirmation_prompt` asks twice.

```python
import click


@click.command()
@click.option("--username", prompt=True, help="Your username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--api-key", prompt="API Key", hide_input=True)
@click.option("--server", prompt="Server address")
def login(username, password, api_key, server):
    """Login to server with credentials."""
    click.echo(f"Logging in {username} at {server}")


if __name__ == "__main__":
    login()
```

## Multiple Values and Counts

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on multiple values and counts](https://realpython.com/search?q=multiple+values+and+counts).
:::

Use `multiple=True` to accept a flag multiple times, and `count=True` to count occurrences of a flag.

```python
import click


@click.command()
@click.option("-v", "--verbose", count=True, help="Verbosity level")
@click.option("--name", multiple=True, help="One or more names")
def process(verbose, name):
    """Process with verbosity and multiple names."""
    click.echo(f"Verbosity level: {verbose}")
    for n in name:
        click.echo(f"Hello, {n}!")
    if verbose >= 2:
        click.echo("Extra verbose output")


if __name__ == "__main__":
    process()
```

Run with: `python app.py -vv --name Alice --name Bob`

## Value Validation with Callbacks

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on value validation with callbacks](https://realpython.com/search?q=value+validation+with+callbacks).
:::

Callbacks validate or transform option values before they reach the function.

```python
import click


def validate_port(ctx, param, value):
    """Validate port is in valid range."""
    if value is not None and not (0 < value <= 65535):
        raise click.BadParameter(f"Invalid port: {value}")
    return value


def validate_file_size(ctx, param, value):
    """Reject files larger than 100MB."""
    import os
    if value and os.path.getsize(value) > 100_000_000:
        raise click.BadParameter("File exceeds 100MB limit")
    return value


@click.command()
@click.option("--port", type=int, callback=validate_port, help="Server port")
@click.option("--file", type=click.Path(exists=True), callback=validate_file_size)
def server(port, file):
    """Start server with validated options."""
    click.echo(f"Starting on port {port}")


if __name__ == "__main__":
    server()
```

## Subcommands with Groups

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on subcommands with groups](https://realpython.com/search?q=subcommands+with+groups).
:::

Use `@click.group()` to create nested command structures like `git commit` or `docker run`.

```python
import click


@click.group()
def cli():
    """CLI with subcommands."""
    pass


@cli.command()
@click.argument("name")
def init(name):
    """Initialize a new project."""
    click.echo(f"Initialized project: {name}")


@cli.command()
@click.argument("url")
@click.option("--depth", type=int, help="Shallow clone depth")
def clone(url, depth):
    """Clone a repository."""
    if depth:
        click.echo(f"Shallow clone {url} at depth {depth}")
    else:
        click.echo(f"Cloning {url}")


@cli.command()
@click.option("-m", "--message", required=True, help="Commit message")
@click.option("--amend", is_flag=True, help="Amend previous commit")
def commit(message, amend):
    """Commit changes."""
    if amend:
        click.echo(f"Amending commit: {message}")
    else:
        click.echo(f"Committing: {message}")


if __name__ == "__main__":
    cli()
```

## Context Passing (pass_context)

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on context passing pass_context](https://realpython.com/search?q=context+passing+pass_context).
:::

Share state between commands using the Click context. `@click.pass_context` passes the context as the first argument.

```python
import click


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    """CLI with shared context."""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.argument("name")
@click.pass_context
def greet(ctx, name):
    """Greet a user."""
    if ctx.obj["DEBUG"]:
        click.echo(f"Debug: greeting {name}")
    click.echo(f"Hello, {name}!")


@cli.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
@click.pass_context
def add(ctx, a, b):
    """Add two numbers."""
    result = a + b
    if ctx.obj["DEBUG"]:
        click.echo(f"Debug: {a} + {b} = {result}")
    click.echo(result)


if __name__ == "__main__":
    cli()
```

## echo and Styling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on echo and styling](https://realpython.com/search?q=echo+and+styling).
:::

Click's `echo()` replaces `print()` with cross-platform Unicode and ANSI color support. Use `secho()` for styled output.

```python
import click


@click.command()
@click.option("--name", default="World")
def hello(name):
    """Demonstrate echo and styling."""

    # Basic output
    click.echo(f"Hello, {name}!")

    # Styled output
    click.secho("Success!", fg="green", bold=True)
    click.secho("Warning!", fg="yellow")
    click.secho("Error!", fg="red", blink=True)

    # Colors
    click.secho("Blue text", fg="blue")
    click.secho("Cyan on magenta", fg="cyan", bg="magenta")

    # Clear screen
    click.clear()


if __name__ == "__main__":
    hello()
```

## Click vs Argparse

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on click vs argparse python](https://realpython.com/search?q=click+vs+argparse+python).
:::

| Feature | Click | Argparse |
|---|---|---|
| Standard library | No (`pip install click`) | Yes |
| Subcommands | `@click.group()` decorator | `add_subparsers()` manual setup |
| Argument types | Rich built-in types (`Path`, `IntRange`, `Choice`) | Basic types + custom converters |
| Prompts | Built-in `prompt=True`, `hide_input`, `confirmation_prompt` | Manual implementation required |
| Multiple values | `multiple=True`, `count=True` | `nargs` + custom `action` |
| Help formatting | Automatic, with colors | Automatic, basic |
| Boolean flags | `is_flag=True` | `action='store_true'` |
| Boilerplate | Minimal (decorators) | Moderate |
| Nesting | `@click.pass_context` | `parents` parameter |
| File validation | `type=click.Path(exists=True)` | Custom `type` function |

```python
# argparse equivalent
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

# click equivalent (more concise)
@click.command()
@click.option("--name", required=True)
@click.option("--verbose", is_flag=True)
def main(name, verbose):
    pass
```

## References

- [Click Documentation](https://click.palletsprojects.com/)
- [Click GitHub Repository](https://github.com/pallets/click/)
- [Click API Reference](https://click.palletsprojects.com/en/stable/api/)
