---
title: Python Interview Cheatsheet
---

# Python Interview Cheatsheet

This page is a curated, question-indexed map into the rest of the cheatsheet. Each entry is a question you are likely to see in a Python interview, followed by a link that jumps directly to the section of the notes that answers it. It is intentionally a navigation layer — the actual explanations, code, and caveats live in the linked sections.

Use it two ways:

- **Drilling a topic:** pick a group (e.g. *Asyncio*) and walk every question.
- **Quick review before an interview:** read the questions, and for any you cannot confidently answer in one or two sentences, click through.

## Python Language Fundamentals

- What does `from __future__ import ...` do, and which future imports still matter? [Print Function](/basic/python-future#print-function) · [Division](/basic/python-future#division) · [Annotations](/basic/python-future#annotations)
- What is `Ellipsis` (`...`) used for in modern Python? [Ellipsis](/basic/python-basic#ellipsis)
- How do `for`/`while` `... else` clauses work? [for ... else ...](/basic/python-basic#for-else) · [while ... else ...](/basic/python-basic#while-else)
- What does `try ... except ... else` do that a plain `try ... except` does not? [try ... except ... else ...](/basic/python-basic#try-except-else)
- How does Python handle Unicode vs bytes, and what is a code point? [Characters](/basic/python-unicode#characters) · [Unicode Code Point](/basic/python-unicode#unicode-code-point)

## Data Structures & Collections

- What is the difference between a shallow copy and a deep copy of a list? [Copy Lists](/basic/python-list#copy-lists-shallow-vs-deep-copy)
- Why can `[[]] * n` surprise you? [Initialize Lists with Multiplication Operator](/basic/python-list#initialize-lists-with-multiplication-operator)
- What is a list comprehension, and when is a generator expression better? [List Comprehensions](/basic/python-list#create-lists-with-list-comprehensions)
- How do you get `(index, value)` pairs while iterating? [enumerate()](/basic/python-list#iterate-with-index-using-enumerate)
- How is a dict iterated, and what does `dict.items()` / `dict.keys()` return? [dict.keys()](/basic/python-dict#get-all-keys-with-dict-keys) · [dict.items()](/basic/python-dict#get-key-value-pairs-with-dict-items)
- `dict.setdefault` vs `collections.defaultdict` — which fits which use case? [setdefault and defaultdict](/basic/python-dict#set-default-values-with-setdefault-and-defaultdict)
- How do you merge two dicts (pre-3.9 and post-3.9)? [Merge Two Dictionaries in Python](/basic/python-dict#merge-two-dictionaries-in-python)
- How would you implement an LRU cache from scratch? [Implement LRU Cache with OrderedDict](/basic/python-dict#implement-lru-cache-with-ordereddict)
- How do you dedupe a list while preserving order? [Remove Duplicates from a List](/basic/python-set#remove-duplicates-from-a-list)
- When would you use `heapq` instead of sorting? [Basic Heap Operations](/basic/python-heap#basic-heap-operations) · [Priority Queue](/basic/python-heap#implement-priority-queue-with-heapq)
- How do you emulate a dict-like object with dunder methods? [Emulate a Dictionary with Special Methods](/basic/python-dict#emulate-a-dictionary-with-special-methods)

## Functions & Decorators

- What do `*args` and `**kwargs` really do, and how do you forward them? [Variable Arguments](/basic/python-func#variable-arguments-args-and-kwargs) · [Unpack Arguments](/basic/python-func#unpack-arguments)
- What is the difference between keyword-only and positional-only arguments? [Keyword-Only Arguments](/basic/python-func#keyword-only-arguments) · [Positional-Only Arguments](/basic/python-func#positional-only-arguments)
- What is a closure, and what does it capture? [Closure](/basic/python-func#closure)
- How do decorators work, and how do you write one that takes arguments? [Decorator](/basic/python-func#decorator) · [Decorator with Arguments](/basic/python-func#decorator-with-arguments)
- `functools.lru_cache` vs `functools.partial` — what do they do? [lru_cache](/basic/python-func#cache-with-lru-cache) · [Partial Functions](/basic/python-func#partial-functions)
- How does `functools.singledispatch` implement function overloading? [singledispatch](/basic/python-func#singledispatch-function-overloading)

## Iterators & Generators

- Generator function vs generator expression — when is each idiomatic? [Generator Function vs Generator Expression](/basic/python-generator#generator-function-vs-generator-expression)
- How do you send a value into a running generator? [Send Values to Generator](/basic/python-generator#send-values-to-generator)
- What does `yield from` do, and how does it compose generators? [yield from Expression](/basic/python-generator#yield-from-expression) · [yield from with Return](/basic/python-generator#yield-from-with-return)
- How do you build an iterable class with a generator method? [Iterable Class via Generator](/basic/python-generator#iterable-class-via-generator)
- How do you implement a context manager as a generator with `@contextmanager`? [Context Manager via Generator](/basic/python-generator#context-manager-via-generator) · [What @contextmanager does](/basic/python-generator#what-contextmanager-does)
- What is an async generator, and how does it differ from a normal generator? [Async Generator](/basic/python-generator#async-generator-python-3-6)

## Classes & OOP

- `__new__` vs `__init__` — when does each run? [__new__ vs __init__](/basic/python-object#new-vs-init)
- `__str__` vs `__repr__` — who calls which? [__str__ and __repr__](/basic/python-object#str-and-repr)
- How does the descriptor protocol work? [Descriptor Protocol](/basic/python-object#descriptor-protocol)
- What is the context manager protocol (`__enter__` / `__exit__`)? [Context Manager Protocol](/basic/python-object#context-manager-protocol)
- `@staticmethod` vs `@classmethod` — when to use which? [staticmethod and classmethod](/basic/python-object#staticmethod-and-classmethod)
- What is MRO, and how does C3 linearization resolve the diamond problem? [The Diamond Problem (MRO)](/basic/python-object#the-diamond-problem-mro)
- When should you define `__slots__`? [__slots__](/basic/python-object#using-slots)
- How do you define a class at runtime with `type(...)`? [Declare Class with type()](/basic/python-object#declare-class-with-type)
- What are abstract base classes, and how does `abc` enforce them? [Abstract Base Classes](/basic/python-object#abstract-base-classes-with-abc)
- How do you implement a callable object? [Callable with __call__](/basic/python-object#callable-with-call)
- What does `@property` buy you over plain getters/setters? [@property Decorator](/basic/python-object#property-decorator)

## Concurrency

- What is the GIL, and how does it affect CPU-bound vs I/O-bound code? [Understanding the GIL](/concurrency/python-threading#understanding-the-gil)
- Threading vs multiprocessing — when would you reach for each? [Creating Threads](/concurrency/python-threading#creating-threads) · [Creating Processes](/concurrency/python-multiprocessing#creating-processes)
- `Lock` vs `RLock` — what is the difference? [Lock](/concurrency/python-threading#lock-mutual-exclusion) · [RLock](/concurrency/python-threading#rlock-reentrant-lock)
- How do you synchronize with `Event`, `Condition`, or `Barrier`? [Event](/concurrency/python-threading#event-thread-signaling) · [Condition](/concurrency/python-threading#condition-complex-synchronization) · [Barrier](/concurrency/python-threading#barrier-synchronization-point)
- How would you build a producer-consumer pipeline with `queue.Queue`? [Producer-Consumer with Queue](/concurrency/python-threading#producer-consumer-with-queue)
- What is a deadlock, and how do you prevent one? [Deadlock Example and Prevention](/concurrency/python-threading#deadlock-example-and-prevention)
- How do you share state across processes (Queue, Pipe, Value, Manager)? [Sharing Data with Queue](/concurrency/python-multiprocessing#sharing-data-with-queue) · [Shared Memory](/concurrency/python-multiprocessing#shared-memory-with-value-and-array) · [Manager](/concurrency/python-multiprocessing#manager-for-complex-shared-objects)
- `ThreadPoolExecutor` vs `ProcessPoolExecutor` — how do you pick? [ThreadPoolExecutor](/concurrency/python-futures#threadpoolexecutor-basics) · [ProcessPoolExecutor](/concurrency/python-futures#processpoolexecutor-basics)
- How do you process results from many futures as they complete? [as_completed](/concurrency/python-futures#processing-results-as-they-complete)

## Asyncio

- What actually happens when you call `asyncio.run(coro())`? [asyncio.run](/asyncio/python-asyncio-basic#running-coroutines-with-asyncio-run)
- `asyncio.create_task` vs awaiting a coroutine directly — what is the difference? [Tasks](/asyncio/python-asyncio-basic#creating-and-managing-tasks)
- How do `asyncio.gather` and `asyncio.wait` differ? [gather](/asyncio/python-asyncio-basic#gathering-multiple-coroutines) · [wait for first completed](/asyncio/python-asyncio-basic#waiting-for-first-completed)
- How do you time-bound an awaitable? [Waiting with Timeout](/asyncio/python-asyncio-basic#waiting-with-timeout)
- What is an async context manager, and how do you write one? [Async Context Managers](/asyncio/python-asyncio-basic#asynchronous-context-managers) · [@asynccontextmanager](/asyncio/python-asyncio-basic#using-asynccontextmanager)
- How do you call blocking code from an async function without blocking the loop? [Running Blocking Code in Executor](/asyncio/python-asyncio-basic#running-blocking-code-in-executor)
- How do you handle exceptions raised inside tasks? [Exception Handling in Tasks](/asyncio/python-asyncio-basic#exception-handling-in-tasks)
- How do you rate-limit concurrency in asyncio? [Semaphores](/asyncio/python-asyncio-advanced#semaphores-for-rate-limiting)
- What is a graceful shutdown in asyncio? [Graceful Shutdown](/asyncio/python-asyncio-advanced#graceful-shutdown)
- Conceptually, what is a coroutine and how does the event loop drive it? [What is a Coroutine?](/asyncio/python-asyncio-guide#what-is-a-coroutine) · [Event Loop](/asyncio/python-asyncio-guide#event-loop)

## Common Gotchas

- Why is using a mutable default argument (`def f(x=[])`) dangerous? [Default Arguments](/basic/python-func#default-arguments)

## C Extensions & Interop

- How do you write a C extension module with the CPython C API? [Simple C Extension](/extension/python-capi#simple-c-extension) · [Parse Arguments](/extension/python-capi#parse-arguments)
- How and why do you release the GIL in a C extension? [Release the GIL](/extension/python-capi#release-the-gil)
- How do you call into a shared library with `ctypes`? [Loading Shared Libraries](/extension/python-ctypes#loading-shared-libraries) · [Basic Type Mapping](/extension/python-ctypes#basic-type-mapping)

## Networking

- How do you resolve a hostname to an IP in Python? [Address Info (DNS Resolution)](/network/python-socket#get-address-info-dns-resolution)
- Network byte order — when and why do you need `htons` / `ntohs`? [Network Byte Order Conversion](/network/python-socket#network-byte-order-conversion)
- How do you build a minimal TLS echo server and client? [Simple TLS Echo Server](/network/python-socket-ssl#simple-tls-echo-server) · [TLS Client](/network/python-socket-ssl#tls-client)
- What is mutual TLS (mTLS), and why would a service require it? [Mutual TLS (mTLS)](/network/python-socket-ssl#mutual-tls-mtls)

## Databases

- What does a SQLAlchemy engine actually hold, and how do connections work? [Create an Engine](/database/python-sqlalchemy#create-an-engine) · [Database URL Format](/database/python-sqlalchemy#database-url-format)
- How do you run raw SQL safely with parameters? [Connect and Execute Raw SQL](/database/python-sqlalchemy#connect-and-execute-raw-sql)
- Transactions in SQLAlchemy — who commits, and when? [Transaction Management](/database/python-sqlalchemy#transaction-management)
- Core vs ORM — what does the ORM add on top? [Declarative Base](/database/python-sqlalchemy-orm#define-models-with-declarative-base) · [Session Basics](/database/python-sqlalchemy-orm#session-basics)

## Security & Crypto

- What are the common cryptographic mistakes to avoid? [Common Mistakes](/security/python-crypto#common-mistakes-dont-do-this) · [Security Checklist](/security/python-crypto#security-checklist)
- Why should you prefer `secrets` over `random` for tokens? [Secure Random Generation](/security/python-crypto#secure-random-generation) · [Weak Random](/security/python-vulnerability#weak-random-number-generation)
- What is a timing attack, and how do you defend against one? [Timing Attacks](/security/python-vulnerability#timing-attacks-on-string-comparison)
- How does SQL injection happen in Python, and how is it prevented? [SQL Injection](/security/python-vulnerability#sql-injection)

## See Also

If a question above is not covered, the top-level indices are the best next stop:

- [Basic](/basic/) — Python core language and data structures
- [Concurrency](/concurrency/) — Threading, multiprocessing, futures
- [Asyncio](/asyncio/) — Asyncio and async patterns
- [Network](/network/) — Sockets and SSL/TLS
- [Database](/database/) — SQLAlchemy core and ORM
- [Security](/security/) — Cryptography and common vulnerabilities
- [Extension](/extension/) — C extensions and FFI
