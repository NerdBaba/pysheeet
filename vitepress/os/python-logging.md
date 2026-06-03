---
title: Logging
---

# Logging

Source  
[src/basic/logging\_.py](https://github.com/crazyguitar/pysheeet/blob/master/src/basic/logging_.py)

[[toc]]

Python's `logging` module provides a flexible framework for emitting log messages from applications and libraries. It supports hierarchical loggers, multiple output handlers, configurable formatting, and severity levels. The module is part of the standard library — no extra dependencies needed. Proper logging is essential for debugging production issues, monitoring system health, and auditing user actions.

## Quick Start with basicConfig

The simplest way to start logging is `basicConfig()`, which sets up a default handler that writes to stderr. Call it once at application startup.

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# These are the five standard log levels
logging.debug("Detailed debug information")
logging.info("General informational messages")
logging.warning("Something unexpected but non-critical")
logging.error("A more serious problem")
logging.critical("A critical error — application may crash")
```

## Log Levels Hierarchy

Each level has a numeric value. A logger set to level `WARNING` will emit messages at `WARNING`, `ERROR`, and `CRITICAL` but suppress `DEBUG` and `INFO`.

| Level | Numeric Value | When to Use |
|---|---|---|
| `DEBUG` | 10 | Detailed diagnostics, variable dumps |
| `INFO` | 20 | Confirmation things work as expected |
| `WARNING` | 30 | Something unexpected but not an error |
| `ERROR` | 40 | A failure, but the app can continue |
| `CRITICAL` | 50 | A fatal error, app may not continue |

```python
import logging

logging.getLogger().setLevel(logging.WARNING)  # Default is WARNING

logging.info("This will NOT appear")       # Below threshold
logging.warning("This WILL appear")         # At threshold
logging.error("This will also appear")      # Above threshold
```

## Logging to a File

Redirect output to a file instead of the console for persistent logs.

```python
import logging

# File output only
logging.basicConfig(
    filename="app.log",
    filemode="a",          # 'a' append (default), 'w' overwrite
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Log to both file and console with separate handlers
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

## Logger Objects vs Root Logger

Always create named loggers instead of using the root logger directly. Named loggers make it clear which module produced a message and give fine-grained control over log levels per module.

```python
import logging

# Root logger — avoid using directly
logging.warning("Root logger — hard to filter by source")

# Named logger — preferred
logger = logging.getLogger(__name__)
logger.info("Named logger — easy to trace to source module")

# Child loggers inherit from parents
parent = logging.getLogger("app")
child = logging.getLogger("app.sub")
child.info("This inherits 'app' logger's handlers and level")
```

## Log Record Attributes

The `format` string supports a wide range of attributes. These are the most commonly used:

```python
import logging

logging.basicConfig(
    format=(
        "%(asctime)s        # Timestamp from datefmt\n"
        "%(name)s           # Logger name (e.g., __name__)\n"
        "%(levelname)s      # DEBUG, INFO, WARNING, ERROR, CRITICAL\n"
        "%(message)s        # The logged message\n"
        "%(filename)s       # Source file (e.g., app.py)\n"
        "%(lineno)d         # Line number in source\n"
        "%(funcName)s       # Function name\n"
        "%(process)d        # Process ID\n"
        "%(threadName)s     # Thread name\n"
    ),
    style="%",  # '%' (default), '{' (str.format), '$' (string.Template)
)
```

## RotatingFileHandler

Prevent log files from growing indefinitely by rotating them when they reach a size limit.

```python
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Rotate by file size
handler = RotatingFileHandler(
    "app.log",
    maxBytes=10_000_000,  # 10 MB per file
    backupCount=5,        # Keep 5 backup files
)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logger = logging.getLogger("my_app")
logger.addHandler(handler)

# Rotate by time interval
time_handler = TimedRotatingFileHandler(
    "app.log",
    when="midnight",   # 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight'
    interval=1,
    backupCount=7,     # Keep 7 days of logs
)
time_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(time_handler)
```

## Logging in Libraries

Libraries should create a named logger and **never** configure handlers themselves — that's the application's responsibility. Use `NullHandler` to suppress "No handler found" warnings when the library is used without logging configured.

```python
# my_lib.py
import logging

logger = logging.getLogger(__name__)

# Add NullHandler so users don't see "No handler" warnings
logging.getLogger(__name__).addHandler(logging.NullHandler())


def do_something():
    logger.info("Library code doing work")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Something went wrong")  # Includes traceback
```

In the application:

```python
# app.py
import logging

logging.basicConfig(level=logging.INFO)

import my_lib

my_lib.do_something()  # Logs appear with the library's logger name
```

## Structured / JSON Logging

Structured logging outputs logs as JSON for easy ingestion by log aggregation systems like Elasticsearch, Datadog, or Splunk. This pattern uses a custom formatter or a library like `python-json-logger`.

```python
import logging
import json


class JSONFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_entry["extra"] = record.extra_data
        return json.dumps(log_entry)


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("json_app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# With extra context
logger.info("User logged in", extra={"extra_data": {"user_id": 42, "ip": "10.0.0.1"}})
```

## Logging Configuration with dictConfig

For complex setups, `dictConfig` allows declarative configuration in a dictionary structure — ideal for configuration files (YAML, JSON) or centralized setup.

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "simple": {
            "format": "%(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "app.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
        },
    },
    "loggers": {
        "my_app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "my_app.library": {
            "level": "WARNING",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("my_app")
logger.info("Logging configured with dictConfig")
```

## Exception Logging

Capture full tracebacks with `logger.exception()` inside exception handlers. It logs at `ERROR` level and includes the traceback automatically.

```python
import logging

logger = logging.getLogger(__name__)

try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Division failed")  # Includes full traceback
    # Alternatively, log at any level with exc_info
    logger.error("Division failed", exc_info=True)
```

## Filtering Logs

Add filters to selectively include or exclude log records based on custom criteria.

```python
import logging


class SensitiveDataFilter(logging.Filter):
    """Filter out log records containing sensitive patterns."""

    def filter(self, record):
        message = record.getMessage()
        return "password" not in message.lower() and "secret" not in message.lower()


logger = logging.getLogger("filtered_app")
logger.addFilter(SensitiveDataFilter())

logger.info("User logged in")          # Appears
logger.info("Password: 12345")         # Filtered out
logger.info("API secret key: abc")     # Filtered out
```

## References

- [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [logging.config — Logging configuration](https://docs.python.org/3/library/logging.config.html)
- [logging.handlers — Logging handlers](https://docs.python.org/3/library/logging.handlers.html)
