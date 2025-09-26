"""
Configuration for pytest tests for the regman package.
"""

# mypy: ignore-errors

from typing import Generator

import pytest

from regman import Registry, RegistryManager


@pytest.fixture
def empty_registry() -> Generator[Registry, None, None]:
    """
    Fixture for an empty registry.

    Returns:
        Registry: An empty registry for tests
    """
    registry = Registry("test_registry")
    yield registry


@pytest.fixture
def populated_registry() -> Generator[Registry, None, None]:
    """
    Fixture for a registry with elements.

    Returns:
        Registry: A registry with elements for tests
    """
    registry = Registry("populated_test_registry")
    registry.add("key1", "value1")
    registry.add("key2", "value2")
    registry.add("key3", "value3")
    yield registry


@pytest.fixture
def empty_manager() -> Generator[RegistryManager, None, None]:
    """
    Fixture for an empty registry manager.

    Returns:
        RegistryManager: An empty registry manager for tests
    """
    manager = RegistryManager()
    yield manager


@pytest.fixture
def populated_manager() -> Generator[RegistryManager, None, None]:
    """
    Fixture for a registry manager with registries.

    Returns:
        RegistryManager: A registry manager with registries for tests
    """
    manager = RegistryManager()
    registry1 = manager.create_registry("registry1")
    registry2 = manager.create_registry("registry2")
    registry1.add("key1", "value1")
    registry2.add("key2", "value2")
    yield manager
