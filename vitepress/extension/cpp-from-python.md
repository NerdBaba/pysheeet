---
title: Learn C++ from Python
---

# Learn C++ from Python

[[toc]]
Modern C++ (C++11, C++14, C++17, C++20) has evolved to include features that make it syntactically similar to Python, making the transition easier for Python developers. This comprehensive guide provides side-by-side comparisons and 1-1 mappings between Python and modern C++ code snippets, covering essential programming concepts like variables, data structures, functions, lambdas, classes, and algorithms.

Whether you're a Python developer looking to learn C++ for performance optimization, system programming, or expanding your programming skills, this tutorial demonstrates how familiar Python patterns translate to modern C++ syntax. Many popular frameworks like PyTorch, TensorFlow, and NumPy use C++ extensions for performance-critical operations, especially in deep learning, LLM training, and CUDA GPU programming. Understanding C++ enables you to write custom extensions, optimize bottlenecks, and contribute to these high-performance libraries.

To learn more about C++ programming, refer to this [C++ cheatsheet](https://cppcheatsheet.com/) for additional reference and best practices.

**Complete working examples:** See [cpp_from_py.cpp](https://github.com/crazyguitar/pysheeet/blob/master/src/cpp_from_python/cpp_from_py.cpp) for runnable code with integrated Google Test suite. Each function includes Doxygen comments showing the equivalent Python code.

## Hello World

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on hello world](https://realpython.com/search?q=hello+world).
:::

The traditional first program in any language. Both Python and C++ can print text to the console, though C++ requires including the iostream library and a main function.

**Python**

```python
print("Hello, World!")
```

**C++**

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

## Variables

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on variables](https://realpython.com/search?q=variables).
:::

Modern C++ supports automatic type inference with the `auto` keyword, making variable declarations as concise as Python. The compiler deduces types from initialization values.

**Python**

```python
x = 10
y = 3.14
name = "Alice"
is_valid = True
```

**C++**

```cpp
auto x = 10;
auto y = 3.14;
auto name = "Alice";
auto is_valid = true;
```

## Lists and Vectors

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp vector python list conversion](https://realpython.com/search?q=cpp+vector+python+list+conversion).
:::

Python lists and C++ vectors are dynamic arrays that can grow and shrink. Both support indexing, appending elements, and querying size. C++ vectors require specifying the element type, but modern C++ can infer it from initialization.

**Python**

```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
print(numbers[0])
print(len(numbers))
```

**C++**

```cpp
#include <vector>

std::vector<int> numbers = {1, 2, 3, 4, 5};
numbers.push_back(6);
std::cout << numbers[0] << std::endl;
std::cout << numbers.size() << std::endl;
```

## Array Slicing and Access

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on array slicing and access](https://realpython.com/search?q=array+slicing+and+access).
:::

Python supports powerful slicing syntax with negative indices and ranges. C++ doesn't have built-in slicing, but you can use iterators or create subvectors. Negative indexing requires manual calculation from the end.

**Python**

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[0])
print(numbers[-1])
print(numbers[2:5])
print(numbers[:3])
print(numbers[7:])
print(numbers[::2])
print(numbers[::-1])
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> numbers = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};

std::cout << numbers[0] << std::endl;
std::cout << numbers[numbers.size() - 1] << std::endl;

std::vector<int> slice1(numbers.begin() + 2, numbers.begin() + 5);
std::vector<int> slice2(numbers.begin(), numbers.begin() + 3);
std::vector<int> slice3(numbers.begin() + 7, numbers.end());

std::vector<int> every_second;
for (size_t i = 0; i < numbers.size(); i += 2) {
    every_second.push_back(numbers[i]);
}

std::vector<int> reversed(numbers.rbegin(), numbers.rend());
```

## Dictionaries and Maps

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on dictionaries and maps](https://realpython.com/search?q=dictionaries+and+maps).
:::

Dictionaries in Python and maps in C++ store key-value pairs. Both allow insertion, lookup, and modification using bracket notation. C++ maps keep keys sorted, while Python dicts maintain insertion order (Python 3.7+).

**Python**

```python
ages = {"Alice": 30, "Bob": 25}
ages["Charlie"] = 35
print(ages["Alice"])
```

**C++**

```cpp
#include <map>
#include <string>

std::map<std::string, int> ages = {{"Alice", 30}, {"Bob", 25}};
ages["Charlie"] = 35;
std::cout << ages["Alice"] << std::endl;
```

## For Loop

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on for loop](https://realpython.com/search?q=for+loop).
:::

Both languages support traditional counting loops and range-based iteration. C++ range-based for loops (C++11) provide syntax similar to Python's for-in loops, making iteration over containers more readable.

**Python**

```python
for i in range(5):
    print(i)

for item in [1, 2, 3]:
    print(item)
```

**C++**

```cpp
for (int i = 0; i < 5; i++) {
    std::cout << i << std::endl;
}

for (auto item : {1, 2, 3}) {
    std::cout << item << std::endl;
}
```

## While Loop

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on while loop](https://realpython.com/search?q=while+loop).
:::

While loops execute as long as a condition is true. The syntax is nearly identical between Python and C++, with C++ requiring parentheses around the condition and braces for the body.

**Python**

```python
i = 0
while i < 5:
    print(i)
    i += 1
```

**C++**

```cpp
int i = 0;
while (i < 5) {
    std::cout << i << std::endl;
    i++;
}
```

## If-Else

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on if-else](https://realpython.com/search?q=if-else).
:::

Conditional statements control program flow based on boolean expressions. C++ requires parentheses around conditions and uses braces for blocks, while Python uses indentation. Both support chained conditions with elif/else if.

**Python**

```python
x = 10
if x > 5:
    print("Greater")
elif x == 5:
    print("Equal")
else:
    print("Less")
```

**C++**

```cpp
auto x = 10;
if (x > 5) {
    std::cout << "Greater" << std::endl;
} else if (x == 5) {
    std::cout << "Equal" << std::endl;
} else {
    std::cout << "Less" << std::endl;
}
```

## Functions

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on functions](https://realpython.com/search?q=functions).
:::

Functions encapsulate reusable code. Modern C++ supports trailing return type syntax (-\> type) similar to Python's type hints. The auto keyword allows type inference for return types when the function body is simple.

**Python**

```python
def add(a, b):
    return a + b

result = add(3, 5)
```

**C++**

```cpp
auto add(int a, int b) -> int {
    return a + b;
}

auto result = add(3, 5);
```

## Lambda Functions

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on lambda functions](https://realpython.com/search?q=lambda+functions).
:::

Lambda functions are anonymous functions that can capture variables from their surrounding scope. Both Python and C++ support lambdas, making functional programming patterns possible. C++ lambdas can specify capture modes (by value, by reference) for more control over variable lifetime and performance.

**Python**

```python
square = lambda x: x * x
print(square(5))

numbers = [1, 2, 3, 4]
squared = list(map(lambda x: x * x, numbers))

# Capturing variables
multiplier = 10
multiply = lambda x: x * multiplier
print(multiply(5))
```

**C++**

```cpp
#include <vector>
#include <algorithm>

auto square = [](int x) { return x * x; };
std::cout << square(5) << std::endl;

std::vector<int> numbers = {1, 2, 3, 4};
std::vector<int> squared;
std::transform(numbers.begin(), numbers.end(),
               std::back_inserter(squared),
               [](int x) { return x * x; });

// Capturing variables by value [=] or by reference [&]
int multiplier = 10;
auto multiply = [multiplier](int x) { return x * multiplier; };
std::cout << multiply(5) << std::endl;
```

## Lambda Capture Modes

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp lambda capture modes](https://realpython.com/search?q=cpp+lambda+capture+modes).
:::

C++ lambdas provide explicit control over how variables are captured from the enclosing scope. This is more explicit than Python's implicit closure behavior and allows optimization by choosing between copying values or using references.

**Python**

```python
x = 10
y = 20

# Implicitly captures x and y
add_xy = lambda z: x + y + z
print(add_xy(5))
```

**C++**

```cpp
int x = 10;
int y = 20;

// Capture by value
auto add_xy_val = [x, y](int z) { return x + y + z; };
std::cout << add_xy_val(5) << std::endl;

// Capture by reference
auto add_xy_ref = [&x, &y](int z) { return x + y + z; };

// Capture all by value
auto add_all_val = [=](int z) { return x + y + z; };

// Capture all by reference
auto add_all_ref = [&](int z) { return x + y + z; };
```

## List Comprehension

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp list comprehension](https://realpython.com/search?q=cpp+list+comprehension).
:::

Python's list comprehensions provide concise syntax for creating lists. C++ doesn't have direct syntax for this, but you can achieve similar results using loops or STL algorithms like std::transform and std::copy_if.

**Python**

```python
squares = [x * x for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> squares;
for (int x = 0; x < 10; x++) {
    squares.push_back(x * x);
}

std::vector<int> evens;
for (int x = 0; x < 10; x++) {
    if (x % 2 == 0) {
        evens.push_back(x);
    }
}
```

## String Operations

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on string operations](https://realpython.com/search?q=string+operations).
:::

Both languages provide rich string manipulation capabilities. C++ strings are mutable like Python strings in terms of concatenation, but individual character access works similarly. C++ requires explicit conversion functions for case changes.

**Python**

```python
s = "Hello"
s += " World"
print(len(s))
print(s[0])
print(s.upper())
```

**C++**

```cpp
#include <string>
#include <algorithm>

std::string s = "Hello";
s += " World";
std::cout << s.size() << std::endl;
std::cout << s[0] << std::endl;

std::string upper = s;
std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
std::cout << upper << std::endl;
```

## Classes

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on classes](https://realpython.com/search?q=classes).
:::

Object-oriented programming works similarly in both languages. C++ requires explicit access specifiers (public, private) and constructor initialization lists. Both support member variables and methods, with C++ using :: for scope resolution.

**Python**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

p = Person("Alice", 30)
print(p.greet())
```

**C++**

```cpp
#include <string>

class Person {
public:
    std::string name;
    int age;

    Person(std::string name, int age) : name(name), age(age) {}

    std::string greet() {
        return "Hello, I'm " + name;
    }
};

Person p("Alice", 30);
std::cout << p.greet() << std::endl;
```

## Optional Values

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp optional python](https://realpython.com/search?q=cpp+optional+python).
:::

Python uses None to represent missing values, while C++ (C++17+) provides std::optional for type-safe optional values. This prevents null pointer errors and makes the absence of a value explicit in the type system.

**Python**

```python
def find_value(key):
    data = {"a": 1, "b": 2}
    return data.get(key)

result = find_value("a")
if result is not None:
    print(result)
```

**C++**

```cpp
#include <optional>
#include <map>

std::optional<int> find_value(std::string key) {
    std::map<std::string, int> data = {{"a", 1}, {"b", 2}};
    auto it = data.find(key);
    if (it != data.end()) {
        return it->second;
    }
    return std::nullopt;
}

auto result = find_value("a");
if (result.has_value()) {
    std::cout << result.value() << std::endl;
}
```

## Smart Pointers

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp smart pointers python](https://realpython.com/search?q=cpp+smart+pointers+python).
:::

Python handles memory automatically with garbage collection. C++ smart pointers (C++11+) provide automatic memory management through RAII. unique_ptr ensures single ownership, while shared_ptr allows multiple owners with reference counting.

**Python**

```python
class Resource:
    def __init__(self, name):
        self.name = name

resource = Resource("data")
```

**C++**

```cpp
#include <memory>

class Resource {
public:
    std::string name;
    Resource(std::string name) : name(name) {}
};

auto resource = std::make_unique<Resource>("data");
auto shared = std::make_shared<Resource>("data");
```

## File I/O

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on file i o](https://realpython.com/search?q=file+i+o).
:::

**Python**

```python
with open("file.txt", "r") as f:
    content = f.read()

with open("file.txt", "w") as f:
    f.write("Hello")
```

**C++**

```cpp
#include <fstream>
#include <string>

std::ifstream file("file.txt");
std::string content((std::istreambuf_iterator<char>(file)),
                    std::istreambuf_iterator<char>());

std::ofstream out("file.txt");
out << "Hello";
```

## Exception Handling

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on exception handling](https://realpython.com/search?q=exception+handling).
:::

Both languages support try-catch exception handling for error management. C++ uses typed exceptions and requires explicit exception types in catch blocks.

**Python**

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Cleanup")
```

**C++**

```cpp
#include <exception>

try {
    if (divisor == 0) {
        throw std::runtime_error("Division by zero");
    }
    result = 10 / divisor;
} catch (const std::exception& e) {
    std::cout << "Error: " << e.what() << std::endl;
}
```

## Tuples

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on tuples](https://realpython.com/search?q=tuples).
:::

Tuples group multiple values together. C++17 introduces structured bindings that allow tuple unpacking similar to Python, making it easy to return and destructure multiple values.

**Python**

```python
point = (10, 20)
x, y = point
print(x, y)
```

**C++**

```cpp
#include <tuple>

auto point = std::make_tuple(10, 20);
auto [x, y] = point;
std::cout << x << " " << y << std::endl;
```

## Enumerate

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on enumerate](https://realpython.com/search?q=enumerate).
:::

Python's enumerate provides index-value pairs during iteration. C++ doesn't have a direct equivalent, but you can achieve the same result with traditional indexed loops.

**Python**

```python
items = ["a", "b", "c"]
for i, item in enumerate(items):
    print(i, item)
```

**C++**

```cpp
#include <vector>
#include <string>

std::vector<std::string> items = {"a", "b", "c"};
for (size_t i = 0; i < items.size(); i++) {
    std::cout << i << " " << items[i] << std::endl;
}
```

## Filter and Map

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on filter and map](https://realpython.com/search?q=filter+and+map).
:::

Python's filter and map functions apply transformations to sequences. C++ provides equivalent functionality through STL algorithms like `std::copy_if` and `std::transform`.

**Python**

```python
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
doubled = list(map(lambda x: x * 2, numbers))
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> numbers = {1, 2, 3, 4, 5};

std::vector<int> evens;
std::copy_if(numbers.begin(), numbers.end(),
             std::back_inserter(evens),
             [](int x) { return x % 2 == 0; });

std::vector<int> doubled;
std::transform(numbers.begin(), numbers.end(),
               std::back_inserter(doubled),
               [](int x) { return x * 2; });
```

## Any and All

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on any and all](https://realpython.com/search?q=any+and+all).
:::

Check if any or all elements in a sequence satisfy a condition. C++ provides `std::any_of` and `std::all_of` algorithms for these common operations.

**Python**

```python
numbers = [1, 2, 3, 4, 5]
has_even = any(x % 2 == 0 for x in numbers)
all_positive = all(x > 0 for x in numbers)
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> numbers = {1, 2, 3, 4, 5};

bool has_even = std::any_of(numbers.begin(), numbers.end(),
                             [](int x) { return x % 2 == 0; });

bool all_positive = std::all_of(numbers.begin(), numbers.end(),
                                 [](int x) { return x > 0; });
```

## Sorting

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on sorting](https://realpython.com/search?q=sorting).
:::

Sort sequences in ascending or descending order. Both languages provide in-place sorting and the ability to create sorted copies with custom comparison functions.

**Python**

```python
numbers = [3, 1, 4, 1, 5]
numbers.sort()

sorted_nums = sorted(numbers, reverse=True)
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> numbers = {3, 1, 4, 1, 5};
std::sort(numbers.begin(), numbers.end());

std::vector<int> sorted_nums = numbers;
std::sort(sorted_nums.begin(), sorted_nums.end(), std::greater<int>());
```

## Min and Max

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on min and max](https://realpython.com/search?q=min+and+max).
:::

Find the minimum and maximum values in a sequence. C++ uses iterator-based algorithms that return iterators, requiring dereferencing to get the actual values.

**Python**

```python
numbers = [3, 1, 4, 1, 5]
print(min(numbers))
print(max(numbers))
```

**C++**

```cpp
#include <vector>
#include <algorithm>

std::vector<int> numbers = {3, 1, 4, 1, 5};
std::cout << *std::min_element(numbers.begin(), numbers.end()) << std::endl;
std::cout << *std::max_element(numbers.begin(), numbers.end()) << std::endl;
```

## Sum

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on sum](https://realpython.com/search?q=sum).
:::

Calculate the sum of all elements in a sequence. C++ uses `std::accumulate` from the numeric library, which can also perform other reduction operations.

**Python**

```python
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
```

**C++**

```cpp
#include <vector>
#include <numeric>

std::vector<int> numbers = {1, 2, 3, 4, 5};
int total = std::accumulate(numbers.begin(), numbers.end(), 0);
```

## Zip

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on zip](https://realpython.com/search?q=zip).
:::

Iterate over multiple sequences in parallel. Python's zip is built-in, while C++ requires manual index-based iteration to achieve the same result.

**Python**

```python
names = ["Alice", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(name, age)
```

**C++**

```cpp
#include <vector>
#include <string>

std::vector<std::string> names = {"Alice", "Bob"};
std::vector<int> ages = {30, 25};

for (size_t i = 0; i < std::min(names.size(), ages.size()); i++) {
    std::cout << names[i] << " " << ages[i] << std::endl;
}
```

## Default Arguments

::: tip Learn More
For more examples and detailed explanations, see [the Real Python guide on cpp default arguments python](https://realpython.com/search?q=cpp+default+arguments+python).
:::

Functions can have default parameter values that are used when arguments aren't provided. Both languages support this feature with similar syntax.

**Python**

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Alice"))
print(greet("Bob", "Hi"))
```

**C++**

```cpp
#include <string>

std::string greet(std::string name, std::string greeting = "Hello") {
    return greeting + ", " + name;
}

std::cout << greet("Alice") << std::endl;
std::cout << greet("Bob", "Hi") << std::endl;
```
