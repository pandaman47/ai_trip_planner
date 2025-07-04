from typing import Optional

def greet(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, Guest!"
    return f"Hello, {name}!"

print(greet())         # Output: Hello, Guest!
print(greet("Alice"))  # Output: Hello, Alice!