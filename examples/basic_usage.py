# mypy: ignore-errors

"""
Basic usage example of the regman package.
"""

from regman import Registry, register, RegistryManager


def main() -> None:
    """Basic usage example."""
    print("=== Basic regman usage example ===\n")

    # 1. Creating a registry
    print("1. Creating a registry")
    registry = Registry("my_registry")
    print(f"Registry created: {registry}")
    print()

    # 2. Adding objects with the add() method
    print("2. Adding objects with add()")
    registry.add("greeting", "Hello world!")
    registry.add("number", 42)
    registry.add("pi", 3.14159)
    print(f"Objects added. Registry size: {len(registry)}")
    print()

    # 3. Retrieving objects
    print("3. Retrieving objects")
    greeting = registry.get("greeting")
    number = registry.get("number")
    pi = registry.get("pi")
    print(f"Greeting: {greeting}")
    print(f"Number: {number}")
    print(f"Pi: {pi}")
    print()

    # 4. Using the decorator
    print("4. Using the @register decorator")

    @register(registry, "calculator")
    class Calculator:
        def add(self, a: int, b: int) -> int:
            return a + b

        def multiply(self, a: int, b: int) -> int:
            return a * b

    # Retrieving and using the class
    CalculatorClass = registry.get("calculator")
    calc = CalculatorClass()
    result_add = calc.add(5, 3)
    result_mult = calc.multiply(4, 7)
    print(f"5 + 3 = {result_add}")
    print(f"4 * 7 = {result_mult}")
    print()

    # 5. Functions with the decorator
    print("5. Functions with the decorator")

    @register(registry, "square")
    def square(x: float) -> float:
        return x * x

    @register(registry, "factorial")
    def factorial(n: int) -> int:
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    square_func = registry.get("square")
    factorial_func = registry.get("factorial")
    print(f"square(5) = {square_func(5)}")
    print(f"factorial(5) = {factorial_func(5)}")
    print()

    # 6. Existence check and listing
    print("6. Existence check and listing")
    print(f"'greeting' exists: {'greeting' in registry}")
    print(f"'nonexistent' exists: {'nonexistent' in registry}")
    print(f"Available keys: {registry.keys()}")
    print(f"Number of elements: {len(registry)}")
    print()

    # 7. Removing elements
    print("7. Removing elements")
    registry.unregister("number")
    print(f"After removing 'number': {len(registry)} elements")
    print(f"Remaining keys: {registry.keys()}")
    print()

    # 8. Clearing the registry
    print("8. Clearing the registry")
    registry.clear()
    print(f"After clearing: {len(registry)} elements")
    print(f"Keys: {registry.keys()}")


if __name__ == "__main__":
    main()
