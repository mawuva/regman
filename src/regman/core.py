"""
Core Registry Module for Regman Package.

This module contains the fundamental Registry class, which is the heart of the
Regman package. The Registry provides a thread-safe, extensible container for
storing and managing objects, functions, classes, or any Python objects by name.

The Registry class is designed to be:
    - Thread-safe: Uses RLock for concurrent access protection
    - Extensible: Supports both decorator and explicit registration patterns
    - Flexible: Can store any type of Python object
    - Easy to use: Provides intuitive API for common operations

Key Features:
    - Thread-safe operations with automatic locking
    - Decorator-based registration for clean code
    - Explicit registration for dynamic scenarios
    - Duplicate key prevention with clear error messages
    - Complete CRUD operations (Create, Read, Update, Delete)
    - Dictionary-like interface with __contains__ and __len__

Registration Patterns:
    1. Decorator pattern (recommended for static registration):
       >>> @registry.register("my_plugin")
       >>> def my_function():
       ...     pass

    2. Decorator with auto-naming:
       >>> @registry.register()
       >>> def another_function():
       ...     pass

    3. Explicit registration:
       >>> registry.add("dynamic_plugin", some_object)

Example Usage:
    >>> from regman import Registry
    >>>
    >>> # Create a registry
    >>> registry = Registry("my_app")
    >>>
    >>> # Register functions using decorators
    >>> @registry.register("processor")
    >>> def process_data(data):
    ...     return data.upper()
    >>>
    >>> # Register classes
    >>> @registry.register("validator")
    >>> class DataValidator:
    ...     def validate(self, data):
    ...         return len(data) > 0
    >>>
    >>> # Access registered objects
    >>> processor = registry.get("processor")
    >>> validator = registry.get("validator")
    >>>
    >>> # Check what's registered
    >>> print(registry.keys())
    >>> print(len(registry))

This module forms the foundation for plugin systems, dependency injection,
service locators, and any pattern requiring centralized object management.
"""

from threading import RLock
from typing import Any, Callable, Dict, List, Optional


class Registry:
    """Registry thread-safe and extensible."""

    def __init__(self, name: str):
        self.name = name
        self._registry_map: Dict[str, Any] = {}
        self._lock = RLock()

    def _register(self, key: str, obj: Any) -> None:
        """Internal method to register a plugin or object in the registry."""
        with self._lock:
            if key in self._registry_map:
                raise ValueError(f"{self.name}: '{key}' already registered.")
            self._registry_map[key] = obj

    def register(self, key: Optional[str] = None) -> Callable:
        """Decorator to register a plugin or object in the registry."""

        def wrapper(obj: Any) -> Any:
            entry_name = key or obj.__name__
            self._register(entry_name, obj)
            return obj

        return wrapper

    def add(self, key: str, obj: Any) -> None:
        """Explicit addition of an object to the registry."""
        self._register(key, obj)

    def unregister(self, key: str) -> None:
        """Remove an entry from the registry."""
        with self._lock:
            self._registry_map.pop(key, None)

    def get(self, key: str) -> Any:
        """Get an object from the registry."""
        with self._lock:
            return self._registry_map[key]

    def keys(self) -> List[str]:
        """Get all keys in the registry."""
        with self._lock:
            return list(self._registry_map.keys())

    def list(self) -> Dict[str, Any]:
        """List all entries."""
        with self._lock:
            return dict(self._registry_map)

    def clear(self) -> None:
        """Clear the registry."""
        with self._lock:
            self._registry_map.clear()

    def __contains__(self, key: str) -> bool:
        """Check if a key is in the registry."""
        with self._lock:
            return key in self._registry_map

    def __len__(self) -> int:
        """Get the number of entries in the registry."""
        with self._lock:
            return len(self._registry_map)

    def __repr__(self) -> str:
        """Get the string representation of the registry."""
        return f"<Registry name={self.name} size={len(self)}>"
