# regman Usage Examples

This folder contains usage examples of the regman package, showing how to use its features in different contexts.

## Available Examples

### 1. `basic_usage.py`
Basic regman usage example:
- Creating a registry
- Adding objects with `add()`
- Using the `@register` decorator
- Retrieving and manipulating objects
- Managing keys and values

### 2. `plugin_system.py`
Complete plugin system example:
- Abstract `Plugin` interface with `ABC`
- Implementation of different plugins (DataProcessor, TextFormatter, DataValidator)
- Plugin manager using regman
- Data processing pipeline

### 3. `strategy_pattern.py`
Strategy pattern implementation example:
- `PaymentStrategy` interface for payment strategies
- Concrete implementations (CreditCard, PayPal, BankTransfer, Cryptocurrency)
- Payment processor using regman
- Cost comparison between strategies

### 4. `observer_pattern.py`
Observer pattern implementation example:
- `Observer` interface for observers
- Concrete implementations (LoggerObserver, EmailNotifier, MetricsCollector)
- `EventSubject` using regman
- Event notification system

### 5. `factory_pattern.py`
Factory pattern implementation example:
- `Animal` interface for animals
- Concrete implementations (Dog, Cat, Bird, Fish)
- `AnimalFactory` using regman
- Zoo simulation

### 6. `concurrent_usage.py`
Concurrent usage example of regman:
- Thread-safe task processor
- Concurrent execution with `ThreadPoolExecutor`
- Multiple registry manager
- Sequential vs concurrent performance tests

## Running Examples

### Run a single example

```bash
# Run a specific example
python examples/basic_usage.py
python examples/plugin_system.py
python examples/strategy_pattern.py
python examples/observer_pattern.py
python examples/factory_pattern.py
python examples/concurrent_usage.py
```

### Run all examples

```bash
# Run all examples with detailed report
python examples/run_all_examples.py
```

The `run_all_examples.py` script:
- Automatically finds all examples
- Runs them in order
- Generates a detailed report with:
  - General summary (success/failures)
  - Execution time
  - Performance statistics
  - Error details (if applicable)
  - Recommendations

## Example Structure

Each example follows a similar structure:

1. **Import dependencies**: Import regman and other necessary modules
2. **Define interfaces**: Use `ABC` and `@abstractmethod` for interfaces
3. **Implement classes**: Concrete classes implementing the interfaces
4. **Register with regman**: Use `@register` to register classes
5. **Use the system**: Demonstrate usage of registered objects
6. **`main()` function**: Main entry point of the example

## Best Practices Demonstrated

- **Abstract interfaces**: Use `ABC` and `@abstractmethod` instead of `raise NotImplementedError`
- **Correct instantiation**: Registered classes are instantiated before use
- **Error handling**: Check key existence before use
- **Thread safety**: Use locks for concurrent operations
- **Documentation**: Detailed docstrings for all functions and classes
- **Type hints**: Type annotations for better readability

## Prerequisites

- Python 3.10+
- regman package installed
- Standard Python modules (threading, abc, typing, etc.)

## Notes

- All examples include `# mypy: ignore-errors` to ignore mypy errors
- Examples are designed to be educational and show best practices
- Each example can be run independently
- Examples use simple test data for demonstration
