# Regman : Thread-Safe Registry Framework for Python

[![CI](https://github.com/mawuva/regman/actions/workflows/ci.yml/badge.svg)](https://github.com/mawuva/regman/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/regman.svg)](https://pypi.org/project/regman/)
[![Python Version](https://img.shields.io/pypi/pyversions/regman.svg)](https://pypi.org/project/regman/)
[![GitHub License](https://img.shields.io/github/license/mawuva/regman)](https://github.com/mawuva/regman/blob/main/LICENSE)

Regman is a lightweight and flexible Python package to manage registries in a thread-safe way. It provides a simple yet powerful infrastructure for registering and managing classes, functions, and objects in a centralized, thread-safe manner.


## Why Regman ?

### The Problem

When building complex Python applications, you often need to:

- **Manage multiple implementations** of the same interface (e.g., different payment methods, data processors, or notification channels)
- **Dynamically select components** at runtime based on configuration or user input
- **Implement design patterns** like Strategy, Factory, Observer, or Plugin architectures
- **Ensure thread safety** when multiple threads access the same registry
- **Avoid tight coupling** between components and their instantiation logic

### Common Solutions and Their Limitations

**Manual dictionaries:**
```python
# ❌ Not thread-safe, error-prone
strategies = {
    "credit_card": CreditCardStrategy,
    "paypal": PayPalStrategy
}
strategy = strategies["credit_card"]()  # KeyError if key doesn't exist
```

**Simple registry classes:**
```python
# ❌ Not thread-safe, basic functionality
class SimpleRegistry:
    def __init__(self):
        self._items = {}
    
    def register(self, key, value):
        self._items[key] = value  # Race condition in multi-threaded apps
```

**Complex dependency injection frameworks:**
```python
# ❌ Overkill for simple use cases, heavy dependencies
from some_di_framework import Container, Service

container = Container()
container.register(Service(IPaymentStrategy), CreditCardStrategy)
# Too much boilerplate for simple registries
```

### The Regman Solution

regman provides a **simple, thread-safe, and flexible** solution:

```python
# ✅ Thread-safe, clean, and powerful
from regman import Registry, register

registry = Registry("payment_strategies")

@register(registry, "credit_card")
class CreditCardStrategy:
    def pay(self, amount):
        return f"Paid ${amount} with credit card"

# Safe to use from multiple threads
strategy_class = registry.get("credit_card")
strategy = strategy_class()
```

### Key Benefits

- **Thread Safety**: Built-in locking ensures safe concurrent access
- **Simplicity**: Clean API with minimal boilerplate
- **Flexibility**: Works with any Python object (classes, functions, instances)
- **Performance**: Optimized for high-frequency access patterns
- **Type Safety**: Full type hints support for better IDE integration
- **Design Pattern Ready**: Perfect for implementing common architectural patterns

### Real-World Use Cases

- **Payment Processing**: Different payment methods (credit card, PayPal, crypto)
- **Plugin Systems**: Dynamic loading and execution of plugins
- **Data Processing Pipelines**: Various data transformers and validators
- **Notification Systems**: Multiple notification channels (email, SMS, push)
- **Configuration Management**: Different configuration providers
- **API Versioning**: Multiple API implementations for different versions

## Features

- **Thread-Safe Registry**: Store and manage objects with automatic locking for concurrent access
- **Registry Manager**: Centralize multiple registries for your project
- **Decorator Support**: Convenient `@register` decorator for easy registration
- **Type Safety**: Full type hints support for better IDE integration
- **Lightweight**: Minimal dependencies, fast performance
- **Flexible**: Works with any Python object (classes, functions, instances)
- **Design Patterns**: Perfect for implementing Strategy, Factory, Observer, and Plugin patterns

## Installation

```bash
pip install regman
```

Or with Poetry:

```bash
poetry add regman
```

## Quick Start

### Basic Usage

```python
from regman import Registry, register

# Create a registry
registry = Registry("my_components")

# Register a class
@register(registry, "calculator")
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

# Register a function
@register(registry, "multiplier")
def multiply(x: float, y: float) -> float:
    return x * y

# Use registered objects
calc_class = registry.get("calculator")
calculator = calc_class()
result = calculator.add(5, 3)  # 8

mult_func = registry.get("multiplier")
result = mult_func(4.5, 2.0)  # 9.0
```

### Registry Manager

```python
from regman import RegistryManager, register

# Create a manager
manager = RegistryManager()

# Create multiple registries
plugins = manager.create_registry("plugins")
strategies = manager.create_registry("strategies")

# Register components
@register(plugins, "data_processor")
class DataProcessor:
    def process(self, data):
        return data * 2

@register(strategies, "payment_credit")
class CreditCardStrategy:
    def pay(self, amount):
        return f"Paid ${amount} with credit card"

# Access registries
data_processor = plugins.get("data_processor")
payment_strategy = strategies.get("payment_credit")
```

## Advanced Usage

### Strategy Pattern

```python
from abc import ABC, abstractmethod
from regman import Registry, register

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

# Register strategies directly
registry = Registry("payment_strategies")

@register(registry, "credit_card")
class CreditCardStrategy(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with credit card"

@register(registry, "paypal")
class PayPalStrategy(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with PayPal"

# Use strategies
strategy_class = registry.get("credit_card")
strategy = strategy_class()
result = strategy.pay(100.0)
```

### Plugin System

```python
from abc import ABC, abstractmethod
from regman import Registry, register

class Plugin(ABC):
    @abstractmethod
    def execute(self, data):
        pass

# Register plugins directly
registry = Registry("plugins")

@register(registry, "data_processor")
class DataProcessor(Plugin):
    def execute(self, data):
        return [x * 2 for x in data]

@register(registry, "text_formatter")
class TextFormatter(Plugin):
    def execute(self, data):
        return str(data).upper()

# Execute plugins
for plugin_name in registry.keys():
    plugin_class = registry.get(plugin_name)
    plugin = plugin_class()
    result = plugin.execute("hello")
```

## API Reference

### Registry

The main registry class for storing and managing objects.

```python
from regman import Registry

registry = Registry("my_registry")
```

#### Methods

- `add(key: str, value: Any) -> None`: Add an object to the registry
- `get(key: str) -> Any`: Retrieve an object from the registry
- `unregister(key: str) -> None`: Remove an object from the registry
- `keys() -> List[str]`: Get all registered keys
- `clear() -> None`: Remove all objects from the registry
- `__contains__(key: str) -> bool`: Check if a key exists
- `__len__() -> int`: Get the number of registered objects

### RegistryManager

Manages multiple registries in a centralized way.

```python
from regman import RegistryManager

manager = RegistryManager()
```

#### Methods

- `create_registry(name: str) -> Registry`: Create a new registry
- `get_registry(name: str) -> Registry`: Get an existing registry
- `all() -> Dict[str, Registry]`: Get all registries

### Decorators

#### @register

Register a class or function with a registry.

```python
from regman import register

@register(registry, "my_key")
class MyClass:
    pass

@register(registry, "my_function")
def my_function():
    pass
```

## Thread Safety

regman is designed to be thread-safe. All registry operations are protected by locks, making it safe to use in multi-threaded environments.

```python
import threading
from regman import Registry, register

registry = Registry("thread_safe")

@register(registry, "worker")
class Worker:
    def work(self):
        return "Working safely!"

# Safe to use from multiple threads
def worker_thread():
    worker_class = registry.get("worker")
    worker = worker_class()
    print(worker.work())

# Start multiple threads
threads = []
for i in range(5):
    thread = threading.Thread(target=worker_thread)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

## Examples

Check out the [examples directory](examples/) for comprehensive usage examples:

- [Basic Usage](examples/basic_usage.py) - Getting started with regman
- [Plugin System](examples/plugin_system.py) - Building a plugin architecture
- [Strategy Pattern](examples/strategy_pattern.py) - Implementing payment strategies
- [Observer Pattern](examples/observer_pattern.py) - Event notification system
- [Factory Pattern](examples/factory_pattern.py) - Object creation patterns
- [Concurrent Usage](examples/concurrent_usage.py) - Multi-threaded applications

Run all examples:

```bash
python examples/run_all_examples.py
```

## Testing

The package includes comprehensive tests covering:

- Unit tests for all components
- Thread safety tests
- Integration tests
- Error handling tests

Run tests:

```bash
# With pytest
pytest tests/

# With poetry
poetry run pytest

# With coverage
pytest --cov=regman tests/
```

## Performance

regman is designed for performance:

- Minimal overhead with efficient locking
- Fast object retrieval with O(1) average case
- Memory efficient with no unnecessary allocations
- Optimized for high-frequency access patterns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/mawuva/regman.git
cd regman

# Install with poetry
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

Run all quality checks:

```bash
poetry run pre-commit run --all-files
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or need help, please:

1. Check the [examples](examples/) directory
2. Read the [documentation](https://github.com/mawuva/regman)
3. Open an [issue](https://github.com/mawuva/regman/issues)

## Acknowledgments

- Inspired by the need for a simple, thread-safe registry system
- Built with modern Python best practices
- Designed for extensibility and performance

