---
title: FastAPI
---

# FastAPI

[[toc]]
FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints. It automatically generates interactive API documentation, performs request validation via Pydantic models, and supports asynchronous request handling out of the box.

## Basic App

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on basic app](https://realpython.com/search?q=basic+app).
:::

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

Run with `uvicorn main:app --reload`. The interactive docs are at `/docs` and the alternative docs at `/redoc`.

## Route Decorators

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on route decorators](https://realpython.com/search?q=route+decorators).
:::

FastAPI maps HTTP methods to Python functions using decorators.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items")
def create_item():
    return {"message": "created"}


@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id}


@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"item_id": item_id}
```

## Path Parameters

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on path parameters](https://realpython.com/search?q=path+parameters).
:::

Path parameters are declared as function parameters in the path. Type hints automatically validate and convert values.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    """Catch-all path parameter."""
    return {"path": file_path}


@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    """Path + optional query parameter."""
    return {"item_id": item_id, "q": q}
```

## Query Parameters

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on query parameters](https://realpython.com/search?q=query+parameters).
:::

Any function parameter not declared in the path is automatically treated as a query parameter.

```python
@app.get("/items")
def list_items(
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    in_stock: bool = False,
):
    return {
        "skip": skip,
        "limit": limit,
        "category": category,
        "in_stock": in_stock,
    }
```

## Request Body with Pydantic Models

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on fastapi pydantic request body](https://realpython.com/search?q=fastapi+pydantic+request+body).
:::

Define request schemas using Pydantic models. FastAPI validates the request body, provides editor autocompletion, and generates JSON Schema for the docs.

```python
from pydantic import BaseModel, Field
from datetime import date

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = None
    tags: list[str] = []
    created_at: date | None = None


class Order(BaseModel):
    items: list[Item]
    user_id: int


@app.post("/items")
def create_item(item: Item):
    return {"item": item, "price_with_tax": item.price * 1.1}


@app.post("/orders")
def create_order(order: Order):
    return {"order_count": len(order.items)}
```

## Query and Path Validators

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on query and path validators](https://realpython.com/search?q=query+and+path+validators).
:::

Use `Query` and `Path` from FastAPI to add validation, metadata, and documentation to parameters.

```python
from fastapi import Query, Path

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000),
    q: str | None = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, alias="page-size"),
):
    return {"item_id": item_id, "q": q, "page": page, "size": size}


@app.get("/search")
def search(
    q: str = Query(..., min_length=2, regex="^[a-zA-Z0-9]+$"),
    deprecated_param: str | None = Query(None, deprecated=True),
):
    return {"query": q}
```

## Dependency Injection

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on fastapi dependency injection](https://realpython.com/search?q=fastapi+dependency+injection).
:::

FastAPI's `Depends` allows you to extract common logic into reusable dependencies.

```python
from fastapi import Depends, HTTPException, Header

# Simple dependency — a function
async def common_params(
    skip: int = 0,
    limit: int = 100,
):
    return {"skip": skip, "limit": limit}


@app.get("/items")
def list_items(params: dict = Depends(common_params)):
    return params


# Class-based dependency
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit


@app.get("/users")
def list_users(pagination: Pagination = Depends()):
    return {"skip": pagination.skip, "limit": pagination.limit}


# Dependency with authentication
async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    return authorization[7:]  # Return the token


@app.get("/protected")
def protected_route(token: str = Depends(verify_token)):
    return {"token": token, "message": "Authenticated"}


# Dependency with yield (resource cleanup)
from contextlib import asynccontextmanager

async def get_db():
    db = await connect_to_database()
    try:
        yield db
    finally:
        await db.close()


@app.get("/data")
def read_data(db=Depends(get_db)):
    return db.query("SELECT * FROM data")
```

::: warning
Dependencies that use `yield` (for cleanup) are only supported in async routes or when using an async-compatible test client.
:::

## Background Tasks

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on background tasks](https://realpython.com/search?q=background+tasks).
:::

Offload work that doesn't need to block the response.

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")


def send_email(email: str, body: str):
    # Simulated email send
    print(f"Sending email to {email}")


@app.post("/users")
def create_user(
    name: str,
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_log, f"User created: {name}")
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "User created", "name": name}
```

## CORS Middleware

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on fastapi cors](https://realpython.com/search?q=fastapi+cors).
:::

Enable CORS so your frontend can call the API from a different origin.

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://myfrontend.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Or allow all origins (development only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Async Route Handlers

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on async route handlers](https://realpython.com/search?q=async+route+handlers).
:::

Use `async def` for routes that perform I/O operations (database queries, HTTP requests, file reads).

```python
import httpx

@app.get("/async-example")
async def async_endpoint():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://httpbin.org/json")
        return resp.json()


@app.get("/concurrent")
async def concurrent_fetch():
    async with httpx.AsyncClient() as client:
        urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/3",
        ]
        tasks = [client.get(url) for url in urls]
        results = await asyncio.gather(*tasks)
    return [r.json() for r in results]
```

::: warning
Avoid mixing `async def` with blocking I/O calls (e.g., `time.sleep`, synchronous file reads). Use `def` for CPU-bound or simple sync logic, and `async def` for async I/O operations.
:::

## File Upload

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on file upload](https://realpython.com/search?q=file+upload).
:::

Handle file uploads with `UploadFile` and `File`.

```python
from fastapi import File, UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }


@app.post("/upload/multiple")
async def upload_multiple(files: list[UploadFile] = File(...)):
    return [
        {
            "filename": f.filename,
            "content_type": f.content_type,
        }
        for f in files
    ]


@app.post("/upload/save")
async def upload_and_save(file: UploadFile = File(...)):
    import aiofiles

    async with aiofiles.open(f"uploads/{file.filename}", "wb") as f:
        while chunk := await file.read(1024):
            await f.write(chunk)

    return {"filename": file.filename, "saved": True}
```

## Error Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on error handling](https://realpython.com/search?q=error+handling).
:::

Raise `HTTPException` for expected errors or register custom exception handlers.

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Item ID must be positive",
        )

    fake_db = {1: "foo", 2: "bar"}
    if item_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Missing item"},
        )

    return {"item": fake_db[item_id]}


@app.get("/divide/{a}/{b}")
def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": a / b}


# Custom exception class
class InsufficientFunds(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount


@app.exception_handler(InsufficientFunds)
def insufficient_funds_handler(request, exc: InsufficientFunds):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=402,
        content={
            "detail": "Insufficient funds",
            "balance": exc.balance,
            "required": exc.amount,
        },
    )
```

## Automatic OpenAPI Docs

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on fastapi openapi docs](https://realpython.com/search?q=fastapi+openapi+docs).
:::

FastAPI generates OpenAPI (Swagger) documentation automatically at `/docs` and `/redoc`. Customize the metadata in the app constructor.

```python
app = FastAPI(
    title="My API",
    description="A sample API with automatic docs",
    version="1.0.0",
    contact={
        "name": "Developer",
        "url": "https://example.com",
        "email": "dev@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "items", "description": "Item operations"},
        {"name": "users", "description": "User operations"},
    ],
)


@app.get("/items", tags=["items"])
def list_items():
    return [{"id": 1, "name": "foo"}]


@app.post("/users", tags=["users"])
def create_user():
    return {"message": "created"}
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial — User Guide](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Starlette Documentation](https://www.starlette.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
