"""
Registry Manager Module for Regman Package.

This module provides the RegistryManager class, which serves as a centralized
container for managing multiple registries within a single project. The manager
allows you to create, access, and organize multiple registries by name, making
it easier to structure complex applications that require different types of
registries for different purposes.

Key Features:
    - Centralized registry management
    - Named registry creation and access
    - Prevention of duplicate registry names
    - Easy enumeration of all managed registries

Example:
    >>> from regman import RegistryManager
    >>> manager = RegistryManager()
    >>>
    >>> # Create different types of registries
    >>> user_registry = manager.create_registry("users")
    >>> product_registry = manager.create_registry("products")
    >>>
    >>> # Access registries by name
    >>> users = manager.get_registry("users")
    >>>
    >>> # List all managed registries
    >>> all_registries = manager.all()

This module is particularly useful for large applications where you need to
organize different types of components, services, or resources into separate
registries while maintaining a single point of control.
"""

from typing import Dict

from regman.core import Registry


class RegistryManager:
    """Centralize multiple registries for a project."""

    def __init__(self) -> None:
        self._registries: Dict[str, Registry] = {}

    def create_registry(self, name: str) -> Registry:
        """Create a new registry."""
        if name in self._registries:
            raise ValueError(f"Registry '{name}' already exists.")
        registry = Registry(name)
        self._registries[name] = registry
        return registry

    def get_registry(self, name: str) -> Registry:  # type: ignore
        """Get a registry."""
        return self._registries[name]

    def all(self) -> Dict[str, Registry]:
        """Get all registries."""
        return dict(self._registries)

    def __repr__(self) -> str:
        """Get the string representation of the registry manager."""
        return f"<RegistryManager registries={list(self._registries.keys())}>"
