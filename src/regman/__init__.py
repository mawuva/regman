"""
Regman: A Thread-Safe Registry Framework for Python

Regman is a powerful and flexible registry framework designed to simplify the
management of objects, plugins, strategies, handlers, and any reusable components
in Python applications. Built with thread-safety as a core principle, Regman
provides a robust foundation for implementing various design patterns including
plugin systems, dependency injection, service locators, and strategy patterns.

Key Features:
    - Thread-safe operations with automatic locking
    - Decorator-based registration for clean, readable code
    - Multiple registry management through RegistryManager
    - Flexible object storage (functions, classes, instances, or any Python object)
    - Duplicate key prevention with clear error messages
    - Dictionary-like interface with intuitive API
    - Extensible architecture for custom registration patterns

Core Components:
    - Registry: The fundamental thread-safe container for object registration
    - RegistryManager: Centralized management of multiple registries
    - register: Convenient decorator for easy object registration

Use Cases:
    - Plugin systems and dynamic loading
    - Strategy pattern implementations
    - Service locator patterns
    - Dependency injection containers
    - Command pattern handlers
    - Factory pattern registries
    - Observer pattern subjects
    - Configuration management

Quick Start:
    >>> from regman import Registry, RegistryManager, register
    >>>
    >>> # Single registry usage
    >>> registry = Registry("my_app")
    >>>
    >>> @registry.register("processor")
    >>> def process_data(data):
    ...     return data.upper()
    >>>
    >>> # Multiple registries management
    >>> manager = RegistryManager()
    >>> user_registry = manager.create_registry("users")
    >>> product_registry = manager.create_registry("products")
    >>>
    >>> # Global registration decorator
    >>> @register("global_handler")
    >>> def handle_request(request):
    ...     return f"Handled: {request}"

Thread Safety:
    All operations are thread-safe using RLock, making Regman suitable for
    multi-threaded applications and concurrent environments.

Version: 0.1.2

For more information, examples, and advanced usage patterns, visit the
project documentation or check the examples directory.
"""

from .core import Registry
from .decorators import register
from .manager import RegistryManager

__version__ = "0.2.0"
__all__ = ["Registry", "register", "RegistryManager"]
