---
title: Learning Path
---

# Learning Path

[[toc]]

A recommended progression through these cheat sheets, organized by skill level and topic area. Whether you're new to Python or brushing up for an interview, follow the path that fits your goals.

## Foundation — Core Python

Start here if you're new to Python or need a refresher on fundamentals.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 1 | [Python Basics](/basic/python-basic) | Syntax, operators, control flow, comprehensions |
| 2 | [Functions](/basic/python-func) | Arguments, decorators, closures, annotations |
| 3 | [Data Structures](/basic/python-dict) | dict, list, set, heap with practical patterns |
| 4 | [Classes & OOP](/basic/python-object) | Inheritance, magic methods, properties, MRO |
| 5 | [Generators](/basic/python-generator) | Generator functions,yield from, async generators |
| 6 | [Type Hints](/basic/python-typing) | Static typing, Protocols, TypedDict, Generics |
| 7 | [Regular Expressions](/basic/python-rexp) | Pattern matching, groups, lookahead |
| 8 | [Unicode](/basic/python-unicode) | Encoding, normalization, bytes vs str |

**Deepen your foundation:**
| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 9 | [Itertools](/basic/python-itertools) | Combinatorics, chaining, grouping, infinite iterators |
| 10 | [Collections](/basic/python-collections) | deque, Counter, defaultdict, namedtuple, ChainMap |
| 11 | [Functools](/basic/python-functools) | partial, cache, singledispatch, wraps, reduce |
| 12 | [Dataclasses](/basic/python-dataclasses) | @dataclass, field, frozen, InitVar, inheritance |

## System & Tools

Apply Python to interact with the operating system and build command-line tools.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 13 | [OS Interfaces](/os/python-os) | Process management, environment, platform info |
| 14 | [Pathlib](/os/python-pathlib) | Modern path manipulation, globbing, file operations |
| 15 | [File I/O](/os/python-io) | Streams, binary data, text encoding |
| 16 | [Date/Time](/os/python-date) | datetime, timezone, formatting, timedelta |
| 17 | [Logging](/os/python-logging) | Log levels, handlers, structured logging |
| 18 | [Argparse](/cli/python-argparse) | CLI argument parsing, subcommands |
| 19 | [Click](/cli/python-click) | Modern CLI framework, commands, groups |

## Concurrent & Async Programming

Master Python's concurrency models for I/O-bound and CPU-bound work.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 20 | [Threading](/concurrency/python-threading) | Threads, locks, queues, GIL implications |
| 21 | [Multiprocessing](/concurrency/python-multiprocessing) | Processes, pools, shared memory |
| 22 | [Futures](/concurrency/python-futures) | ThreadPoolExecutor, ProcessPoolExecutor |
| 23 | [Async Guide](/asyncio/python-asyncio-guide) | Coroutines, event loop, async/await mental model |
| 24 | [Async Basics](/asyncio/python-asyncio-basic) | asyncio.run, tasks, gather, timeouts |
| 25 | [Async Servers](/asyncio/python-asyncio-server) | TCP/UDP servers, streams |
| 26 | [Async Advanced](/asyncio/python-asyncio-advanced) | Semaphores, queues, graceful shutdown |

## Network Programming

Build networked applications from raw sockets to secure communications.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 27 | [Socket Basics](/network/python-socket) | Address resolution, TCP/UDP, byte order |
| 28 | [Socket Servers](/network/python-socket-server) | select, poll, epoll, ThreadingTCPServer |
| 29 | [Async Sockets](/network/python-socket-async) | Non-blocking I/O, async operations |
| 30 | [SSL/TLS](/network/python-socket-ssl) | Secure connections, context configuration |
| 31 | [SSH](/network/python-ssh) | paramiko, key management, tunneling |
| 32 | [Socket Sniffer](/network/python-socket-sniffer) | Raw sockets, packet capture |

## Data & Web

Work with databases, build web APIs, and manipulate data.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 33 | [SQLAlchemy](/database/python-sqlalchemy) | Engine, connections, transactions, raw SQL |
| 34 | [SQLAlchemy ORM](/database/python-sqlalchemy-orm) | Models, relationships, sessions |
| 35 | [SQLAlchemy Query](/database/python-sqlalchemy-query) | Joins, subqueries, aggregation patterns |
| 36 | [FastAPI](/web/python-fastapi) | Routes, Pydantic, DI, async handlers |
| 37 | [NumPy](/data-science/python-numpy) | Arrays, broadcasting, linear algebra, ufuncs |
| 38 | [Pandas](/data-science/python-pandas) | DataFrames, groupby, merge, pivot, datetime |

## Quality & Security

Test your code and keep it secure.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 39 | [Pytest](/testing/python-pytest) | Fixtures, parametrize, tmp_path, monkeypatch |
| 40 | [Unittest Mock](/testing/python-unittest-mock) | patch, Mock, AsyncMock, autospec |
| 41 | [Profiling](/basic/python-profiling) | cProfile, timeit, memory_profiler, optimization |
| 42 | [Cryptography](/security/python-crypto) | AES-GCM, Argon2, key derivation |
| 43 | [TLS/SSL](/security/python-tls) | Certificate verification, secure defaults |
| 44 | [Vulnerabilities](/security/python-vulnerability) | Injection, timing attacks, secure coding |

## Advanced Topics

Specialized areas for ML engineering, high-performance computing, and language extensions.

| Step | Topic | What You'll Learn |
|------|-------|-------------------|
| 45 | [C Extensions](/extension/python-cext-modern) | pybind11, Cython, ctypes comparisons |
| 46 | [PyTorch](/llm/pytorch) | Tensors, autograd, DataLoader, distributed |
| 47 | [Megatron](/llm/megatron) | Model/pipeline parallelism, distributed training |
| 48 | [LLM Serving](/llm/llm-serving) | vLLM, SGLang, continuous batching |
| 49 | [LLM Benchmarks](/llm/llm-bench) | Throughput, latency, benchmarking methodology |
| 50 | [Slurm](/hpc/slurm) | Job submission, GPU scheduling, array jobs |
| 51 | [Ray](/hpc/ray) | Distributed tasks, actors, cluster management |

## Quick Paths by Goal

### Interview Preparation

1. [Interview Cheatsheet](/interview/) — question-indexed map
2. Follow links into each topic area for detailed answers
3. Focus on: OOP ([classes](/basic/python-object)), concurrency ([threading](/concurrency/python-threading), [GIL](/concurrency/python-threading#understanding-the-gil)), [asyncio](/asyncio/python-asyncio-guide), [decorators](/basic/python-func#decorator), [generators](/basic/python-generator), [SQLAlchemy](/database/python-sqlalchemy-orm)

### Data Science / ML

1. [NumPy](/data-science/python-numpy) → [Pandas](/data-science/python-pandas)
2. [PyTorch](/llm/pytorch) → [Megatron](/llm/megatron) → [LLM Serving](/llm/llm-serving)
3. [Slurm](/hpc/slurm) for cluster scheduling

### Systems / Infrastructure

1. [OS](/os/python-os) → [Pathlib](/os/python-pathlib) → [Logging](/os/python-logging)
2. [CLI tools](/cli/python-argparse) → [Click](/cli/python-click)
3. [Network](/network/python-socket) → [SSL/TLS](/network/python-socket-ssl) → [SSH](/network/python-ssh)
4. [Security](/security/python-crypto) → [Vulnerabilities](/security/python-vulnerability)

## See Also

- [Python 3 new features](/python-new-py3) — what changed between versions
- [What's New in Python 3](/python-new-py3) — version-by-version highlights
