---
title: Python Interview Cheatsheet
---

# Python Interview Cheatsheet

This page is a curated, question-indexed map into the rest of the cheatsheet. Each entry is a question you are likely to see in a Python interview, followed by a link that jumps directly to the section of the notes that answers it. It is intentionally a navigation layer — the actual explanations, code, and caveats live in the linked sections.

Use it two ways:

- **Drilling a topic:** pick a group (e.g. *Asyncio*) and walk every question.
- **Quick review before an interview:** read the questions, and for any you cannot confidently answer in one or two sentences, click through.

## Python Language Fundamentals

- What does `from __future__ import ...` do, and which future imports still matter? `→ basic/python-future: Print Function <notes/basic/python-future:Print Function>` · `Division <notes/basic/python-future:Division>` · `Annotations <notes/basic/python-future:Annotations>`
- What is `Ellipsis` (`...`) used for in modern Python? `→ basic/python-basic: Ellipsis <notes/basic/python-basic:Ellipsis>`
- How do `for`/`while` `... else` clauses work? `→ basic/python-basic: for ... else ... <notes/basic/python-basic:for ... else ...>` · `while ... else ... <notes/basic/python-basic:while ... else ...>`
- What does `try ... except ... else` do that a plain `try ... except` does not? `→ basic/python-basic: try ... except ... else ... <notes/basic/python-basic:try ... except ... else ...>`
- How does Python handle Unicode vs bytes, and what is a code point? `→ basic/python-unicode: Characters <notes/basic/python-unicode:Characters>` · `Unicode Code Point <notes/basic/python-unicode:Unicode Code Point>`

## Data Structures & Collections

- What is the difference between a shallow copy and a deep copy of a list? `→ basic/python-list: Copy Lists <notes/basic/python-list:Copy Lists: Shallow vs Deep Copy>`
- Why can `[[]] * n` surprise you? `→ basic/python-list: Initialize Lists with Multiplication Operator <notes/basic/python-list:Initialize Lists with Multiplication Operator>`
- What is a list comprehension, and when is a generator expression better? `→ basic/python-list: List Comprehensions <notes/basic/python-list:Create Lists with List Comprehensions>`
- How do you get `(index, value)` pairs while iterating? `→ basic/python-list: enumerate() <notes/basic/python-list:Iterate with Index Using enumerate()>`
- How is a dict iterated, and what does `dict.items()` / `dict.keys()` return? `` → basic/python-dict: dict.keys() <notes/basic/python-dict:Get All Keys with \`\`dict.keys()\`\`> `` · `` dict.items() <notes/basic/python-dict:Get Key-Value Pairs with \`\`dict.items()\`\`> ``
- `dict.setdefault` vs `collections.defaultdict` — which fits which use case? `` → basic/python-dict: setdefault and defaultdict <notes/basic/python-dict:Set Default Values with \`\`setdefault()\`\` and \`\`defaultdict\`\`> ``
- How do you merge two dicts (pre-3.9 and post-3.9)? `→ basic/python-dict: Merge Two Dictionaries in Python <notes/basic/python-dict:Merge Two Dictionaries in Python>`
- How would you implement an LRU cache from scratch? `→ basic/python-dict: Implement LRU Cache with OrderedDict <notes/basic/python-dict:Implement LRU Cache with OrderedDict>`
- How do you dedupe a list while preserving order? `→ basic/python-set: Remove Duplicates from a List <notes/basic/python-set:Remove Duplicates from a List>`
- When would you use `heapq` instead of sorting? `→ basic/python-heap: Basic Heap Operations <notes/basic/python-heap:Basic Heap Operations>` · `` Priority Queue <notes/basic/python-heap:Implement Priority Queue with \`\`heapq\`\`> ``
- How do you emulate a dict-like object with dunder methods? `→ basic/python-dict: Emulate a Dictionary with Special Methods <notes/basic/python-dict:Emulate a Dictionary with Special Methods>`

## Functions & Decorators

- What do `*args` and `**kwargs` really do, and how do you forward them? `` → basic/python-func: Variable Arguments <notes/basic/python-func:Variable Arguments \`\`*args\`\` and \`\`**kwargs\`\`> `` · `Unpack Arguments <notes/basic/python-func:Unpack Arguments>`
- What is the difference between keyword-only and positional-only arguments? `→ basic/python-func: Keyword-Only Arguments <notes/basic/python-func:Keyword-Only Arguments>` · `Positional-Only Arguments <notes/basic/python-func:Positional-Only Arguments>`
- What is a closure, and what does it capture? `→ basic/python-func: Closure <notes/basic/python-func:Closure>`
- How do decorators work, and how do you write one that takes arguments? `→ basic/python-func: Decorator <notes/basic/python-func:Decorator>` · `Decorator with Arguments <notes/basic/python-func:Decorator with Arguments>`
- `functools.lru_cache` vs `functools.partial` — what do they do? `` → basic/python-func: lru_cache <notes/basic/python-func:Cache with \`\`lru_cache\`\`> `` · `Partial Functions <notes/basic/python-func:Partial Functions>`
- How does `functools.singledispatch` implement function overloading? `` → basic/python-func: singledispatch <notes/basic/python-func:\`\`singledispatch\`\` - Function Overloading> ``

## Iterators & Generators

- Generator function vs generator expression — when is each idiomatic? `→ basic/python-generator: Generator Function vs Generator Expression <notes/basic/python-generator:Generator Function vs Generator Expression>`
- How do you send a value into a running generator? `→ basic/python-generator: Send Values to Generator <notes/basic/python-generator:Send Values to Generator>`
- What does `yield from` do, and how does it compose generators? `→ basic/python-generator: yield from Expression <notes/basic/python-generator:yield from Expression>` · `yield from with Return <notes/basic/python-generator:yield from with Return>`
- How do you build an iterable class with a generator method? `→ basic/python-generator: Iterable Class via Generator <notes/basic/python-generator:Iterable Class via Generator>`
- How do you implement a context manager as a generator with `@contextmanager`? `→ basic/python-generator: Context Manager via Generator <notes/basic/python-generator:Context Manager via Generator>` · `` What @contextmanager does <notes/basic/python-generator:What \`\`@contextmanager\`\` Does> ``
- What is an async generator, and how does it differ from a normal generator? `→ basic/python-generator: Async Generator <notes/basic/python-generator:Async Generator (Python 3.6+)>`

## Classes & OOP

- `__new__` vs `__init__` — when does each run? `→ basic/python-object: __new__ vs __init__ <notes/basic/python-object:__new__ vs __init__>`
- `__str__` vs `__repr__` — who calls which? `→ basic/python-object: __str__ and __repr__ <notes/basic/python-object:__str__ and __repr__>`
- How does the descriptor protocol work? `→ basic/python-object: Descriptor Protocol <notes/basic/python-object:Descriptor Protocol>`
- What is the context manager protocol (`__enter__` / `__exit__`)? `→ basic/python-object: Context Manager Protocol <notes/basic/python-object:Context Manager Protocol>`
- `@staticmethod` vs `@classmethod` — when to use which? `→ basic/python-object: staticmethod and classmethod <notes/basic/python-object:@staticmethod and @classmethod>`
- What is MRO, and how does C3 linearization resolve the diamond problem? `→ basic/python-object: The Diamond Problem (MRO) <notes/basic/python-object:The Diamond Problem (MRO)>`
- When should you define `__slots__`? `→ basic/python-object: __slots__ <notes/basic/python-object:Using __slots__>`
- How do you define a class at runtime with `type(...)`? `→ basic/python-object: Declare Class with type() <notes/basic/python-object:Declare Class with type()>`
- What are abstract base classes, and how does `abc` enforce them? `→ basic/python-object: Abstract Base Classes <notes/basic/python-object:Abstract Base Classes with abc>`
- How do you implement a callable object? `→ basic/python-object: Callable with __call__ <notes/basic/python-object:Callable with __call__>`
- What does `@property` buy you over plain getters/setters? `→ basic/python-object: @property Decorator <notes/basic/python-object:@property Decorator>`

## Concurrency

- What is the GIL, and how does it affect CPU-bound vs I/O-bound code? `→ concurrency/python-threading: Understanding the GIL <notes/concurrency/python-threading:Understanding the GIL>`
- Threading vs multiprocessing — when would you reach for each? `→ concurrency/python-threading: Creating Threads <notes/concurrency/python-threading:Creating Threads>` · `multiprocessing: Creating Processes <notes/concurrency/python-multiprocessing:Creating Processes>`
- `Lock` vs `RLock` — what is the difference? `→ concurrency/python-threading: Lock <notes/concurrency/python-threading:Lock - Mutual Exclusion>` · `RLock <notes/concurrency/python-threading:RLock - Reentrant Lock>`
- How do you synchronize with `Event`, `Condition`, or `Barrier`? `→ concurrency/python-threading: Event <notes/concurrency/python-threading:Event - Thread Signaling>` · `Condition <notes/concurrency/python-threading:Condition - Complex Synchronization>` · `Barrier <notes/concurrency/python-threading:Barrier - Synchronization Point>`
- How would you build a producer-consumer pipeline with `queue.Queue`? `→ concurrency/python-threading: Producer-Consumer with Queue <notes/concurrency/python-threading:Producer-Consumer with Queue>`
- What is a deadlock, and how do you prevent one? `→ concurrency/python-threading: Deadlock Example and Prevention <notes/concurrency/python-threading:Deadlock Example and Prevention>`
- How do you share state across processes (Queue, Pipe, Value, Manager)? `→ concurrency/python-multiprocessing: Sharing Data with Queue <notes/concurrency/python-multiprocessing:Sharing Data with Queue>` · `Shared Memory <notes/concurrency/python-multiprocessing:Shared Memory with Value and Array>` · `Manager <notes/concurrency/python-multiprocessing:Manager for Complex Shared Objects>`
- `ThreadPoolExecutor` vs `ProcessPoolExecutor` — how do you pick? `→ concurrency/python-futures: ThreadPoolExecutor <notes/concurrency/python-futures:ThreadPoolExecutor Basics>` · `ProcessPoolExecutor <notes/concurrency/python-futures:ProcessPoolExecutor Basics>`
- How do you process results from many futures as they complete? `→ concurrency/python-futures: as_completed <notes/concurrency/python-futures:Processing Results as They Complete>`

## Asyncio

- What actually happens when you call `asyncio.run(coro())`? `→ asyncio/python-asyncio-basic: asyncio.run <notes/asyncio/python-asyncio-basic:Running Coroutines with asyncio.run>`
- `asyncio.create_task` vs awaiting a coroutine directly — what is the difference? `→ asyncio/python-asyncio-basic: Tasks <notes/asyncio/python-asyncio-basic:Creating and Managing Tasks>`
- How do `asyncio.gather` and `asyncio.wait` differ? `→ asyncio/python-asyncio-basic: gather <notes/asyncio/python-asyncio-basic:Gathering Multiple Coroutines>` · `wait for first completed <notes/asyncio/python-asyncio-basic:Waiting for First Completed>`
- How do you time-bound an awaitable? `→ asyncio/python-asyncio-basic: Waiting with Timeout <notes/asyncio/python-asyncio-basic:Waiting with Timeout>`
- What is an async context manager, and how do you write one? `→ asyncio/python-asyncio-basic: Async Context Managers <notes/asyncio/python-asyncio-basic:Asynchronous Context Managers>` · `@asynccontextmanager <notes/asyncio/python-asyncio-basic:Using @asynccontextmanager>`
- How do you call blocking code from an async function without blocking the loop? `→ asyncio/python-asyncio-basic: Running Blocking Code in Executor <notes/asyncio/python-asyncio-basic:Running Blocking Code in Executor>`
- How do you handle exceptions raised inside tasks? `→ asyncio/python-asyncio-basic: Exception Handling in Tasks <notes/asyncio/python-asyncio-basic:Exception Handling in Tasks>`
- How do you rate-limit concurrency in asyncio? `→ asyncio/python-asyncio-advanced: Semaphores <notes/asyncio/python-asyncio-advanced:Semaphores for Rate Limiting>`
- What is a graceful shutdown in asyncio? `→ asyncio/python-asyncio-advanced: Graceful Shutdown <notes/asyncio/python-asyncio-advanced:Graceful Shutdown>`
- Conceptually, what is a coroutine and how does the event loop drive it? `→ asyncio/python-asyncio-guide: What is a Coroutine? <notes/asyncio/python-asyncio-guide:What is a Coroutine?>` · `Event Loop <notes/asyncio/python-asyncio-guide:Event Loop>`

## Common Gotchas

- Why is using a mutable default argument (`def f(x=[])`) dangerous? `→ basic/python-func: Default Arguments <notes/basic/python-func:Default Arguments>`

## C Extensions & Interop

- How do you write a C extension module with the CPython C API? `→ extension/python-capi: Simple C Extension <notes/extension/python-capi:Simple C Extension>` · `Parse Arguments <notes/extension/python-capi:Parse Arguments>`
- How and why do you release the GIL in a C extension? `→ extension/python-capi: Release the GIL <notes/extension/python-capi:Release the GIL>`
- How do you call into a shared library with `ctypes`? `→ extension/python-ctypes: Loading Shared Libraries <notes/extension/python-ctypes:Loading Shared Libraries>` · `Basic Type Mapping <notes/extension/python-ctypes:Basic Type Mapping>`

## Networking

- How do you resolve a hostname to an IP in Python? `→ network/python-socket: Address Info (DNS Resolution) <notes/network/python-socket:Get Address Info (DNS Resolution)>`
- Network byte order — when and why do you need `htons` / `ntohs`? `→ network/python-socket: Network Byte Order Conversion <notes/network/python-socket:Network Byte Order Conversion>`
- How do you build a minimal TLS echo server and client? `→ network/python-socket-ssl: Simple TLS Echo Server <notes/network/python-socket-ssl:Simple TLS Echo Server>` · `TLS Client <notes/network/python-socket-ssl:TLS Client>`
- What is mutual TLS (mTLS), and why would a service require it? `→ network/python-socket-ssl: Mutual TLS (mTLS) <notes/network/python-socket-ssl:Mutual TLS (mTLS)>`

## Databases

- What does a SQLAlchemy engine actually hold, and how do connections work? `→ database/python-sqlalchemy: Create an Engine <notes/database/python-sqlalchemy:Create an Engine>` · `Database URL Format <notes/database/python-sqlalchemy:Database URL Format>`
- How do you run raw SQL safely with parameters? `→ database/python-sqlalchemy: Connect and Execute Raw SQL <notes/database/python-sqlalchemy:Connect and Execute Raw SQL>`
- Transactions in SQLAlchemy — who commits, and when? `→ database/python-sqlalchemy: Transaction Management <notes/database/python-sqlalchemy:Transaction Management>`
- Core vs ORM — what does the ORM add on top? `→ database/python-sqlalchemy-orm: Declarative Base <notes/database/python-sqlalchemy-orm:Define Models with Declarative Base>` · `Session Basics <notes/database/python-sqlalchemy-orm:Session Basics>`

## Security & Crypto

- What are the common cryptographic mistakes to avoid? `→ security/python-crypto: Common Mistakes <notes/security/python-crypto:Common Mistakes (Don't Do This)>` · `Security Checklist <notes/security/python-crypto:Security Checklist>`
- Why should you prefer `secrets` over `random` for tokens? `→ security/python-crypto: Secure Random Generation <notes/security/python-crypto:Secure Random Generation>` · `Weak Random <notes/security/python-vulnerability:Weak Random Number Generation>`
- What is a timing attack, and how do you defend against one? `→ security/python-vulnerability: Timing Attacks <notes/security/python-vulnerability:Timing Attacks on String Comparison>`
- How does SQL injection happen in Python, and how is it prevented? `→ security/python-vulnerability: SQL Injection <notes/security/python-vulnerability:SQL Injection>`

## See Also

If a question above is not covered, the top-level indices are the best next stop:

- `../basic/index` — Python core language and data structures
- `../concurrency/index` — Threading, multiprocessing, futures
- `../asyncio/index` — Asyncio and async patterns
- `../network/index` — Sockets and SSL/TLS
- `../database/index` — SQLAlchemy core and ORM
- `../security/index` — Cryptography and common vulnerabilities
- `../extension/index` — C extensions and FFI
