"""
Decorators module for the Regman package.
"""

from typing import Any, Callable, Optional

from .core import Registry


def register(registry: Registry, key: Optional[str] = None) -> Callable:
    """Universal decorator to register in any Registry."""

    def decorator(obj: Any) -> Any:
        registry.add(key or obj.__name__, obj)
        return obj

    return decorator
