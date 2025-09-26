"""
Unit tests for the module manager.py - Class RegistryManager.
"""

# mypy: ignore-errors

import pytest

from regman.core import Registry
from regman.manager import RegistryManager


class TestRegistryManager:
    """Tests for the RegistryManager class."""

    def test_init(self) -> None:
        """
        Scenario: Initialization of a new registry manager

        Expected:
        - The manager is empty
        - No registry is created
        - The string representation is correct
        """
        manager = RegistryManager()
        assert len(manager.all()) == 0
        assert repr(manager) == "<RegistryManager registries=[]>"

    def test_create_registry(self) -> None:
        """
        Scenario: Creation of a new registry

        Expected:
        - The registry is created with the given name
        - The registry is accessible via get_registry()
        - The registry appears in all()
        - The registry is empty
        """
        manager = RegistryManager()
        registry = manager.create_registry("test_registry")

        assert isinstance(registry, Registry)
        assert registry.name == "test_registry"
        assert manager.get_registry("test_registry") is registry
        assert "test_registry" in manager.all()
        assert len(registry) == 0

    def test_create_multiple_registries(self) -> None:
        """
        Scenario: Creation of multiple registries

        Expected:
        - All registries are created correctly
        - Each registry is accessible with its name
        - All registries appear in all()
        - The registries are independent
        """
        manager = RegistryManager()
        registry1 = manager.create_registry("registry1")
        registry2 = manager.create_registry("registry2")
        registry3 = manager.create_registry("registry3")

        assert len(manager.all()) == 3
        assert manager.get_registry("registry1") is registry1
        assert manager.get_registry("registry2") is registry2
        assert manager.get_registry("registry3") is registry3

        # Verify the independence of the registries
        registry1.add("key1", "value1")
        assert len(registry1) == 1
        assert len(registry2) == 0
        assert len(registry3) == 0

    def test_create_registry_duplicate_name_raises_error(self) -> None:
        """
        Scenario: Attempt to create a registry with an already existing name

        Expected:
        - A ValueError is raised
        - The error message contains the name of the registry
        """
        manager = RegistryManager()
        manager.create_registry("duplicate_name")

        with pytest.raises(
            ValueError, match="Registry 'duplicate_name' already exists."
        ):
            manager.create_registry("duplicate_name")

    def test_get_registry_existing(self) -> None:
        """
        Scenario: Retrieval of an existing registry

        Expected:
        - Le registre correct est retourné
        - Le registre retourné est le même que celui créé
        """
        manager = RegistryManager()
        created_registry = manager.create_registry("test_registry")
        retrieved_registry = manager.get_registry("test_registry")

        assert retrieved_registry is created_registry
        assert isinstance(retrieved_registry, Registry)
        assert retrieved_registry.name == "test_registry"

    def test_get_registry_nonexistent_raises_keyerror(self) -> None:
        """
        Scenario: Attempt to retrieve a nonexistent registry

        Expected:
        - A KeyError is raised
        """
        manager = RegistryManager()

        with pytest.raises(KeyError):
            manager.get_registry("nonexistent_registry")

    def test_all_returns_copy(self) -> None:
        """
        Scenario: Modification of the dictionary returned by all() does not modify the manager

        Expected:
        - all() returns a copy of the dictionary
        - Modification of the returned dictionary does not affect the manager
        """
        manager = RegistryManager()
        manager.create_registry("test_registry")

        all_registries = manager.all()
        all_registries["fake_registry"] = "fake_value"

        assert len(manager.all()) == 1
        assert "fake_registry" not in manager.all()
        assert "test_registry" in manager.all()

    def test_all_returns_correct_registries(self) -> None:
        """
        Scenario: Verification of the content of the dictionary returned by all()

        Expected:
        - The dictionary contains all the created registries
        - The keys are the names of the registries
        - The values are the instances of Registry
        """
        manager = RegistryManager()
        registry1 = manager.create_registry("registry1")
        registry2 = manager.create_registry("registry2")

        all_registries = manager.all()

        assert isinstance(all_registries, dict)
        assert len(all_registries) == 2
        assert "registry1" in all_registries
        assert "registry2" in all_registries
        assert all_registries["registry1"] is registry1
        assert all_registries["registry2"] is registry2

    def test_repr_with_no_registries(self) -> None:
        """
        Scenario: String representation of the manager without registries

        Expected:
        - The representation contains an empty list of registries
        """
        manager = RegistryManager()
        assert repr(manager) == "<RegistryManager registries=[]>"

    def test_repr_with_registries(self) -> None:
        """
        Scenario: String representation of the manager with registries

        Expected:
        - The representation contains the list of registry names
        - The order may vary but all names must be present
        """
        manager = RegistryManager()
        manager.create_registry("registry1")
        manager.create_registry("registry2")
        manager.create_registry("registry3")

        repr_str = repr(manager)
        assert "RegistryManager" in repr_str
        assert "registry1" in repr_str
        assert "registry2" in repr_str
        assert "registry3" in repr_str

    def test_registry_independence(self) -> None:
        """
        Scenario: Verification of the independence of the managed registries

        Expected:
        - The registries are completely independent
        - Operations on a registry do not affect the others
        - Each registry has its own state
        """
        manager = RegistryManager()
        registry1 = manager.create_registry("registry1")
        registry2 = manager.create_registry("registry2")

        # Add elements to registry1
        registry1.add("key1", "value1")
        registry1.add("key2", "value2")

        # Verify that registry2 is not affected
        assert len(registry1) == 2
        assert len(registry2) == 0
        assert "key1" in registry1
        assert "key1" not in registry2

        # Add elements to registry2
        registry2.add("key3", "value3")

        # Verify that registry1 is not affected
        assert len(registry1) == 2
        assert len(registry2) == 1
        assert "key3" in registry2
        assert "key3" not in registry1

    def test_registry_operations_through_manager(self) -> None:
        """
        Scenario: Usage of the registries via the manager

        Expected:
        - The registries work normally via the manager
        - The operations of addition, deletion, retrieval function
        - The registries maintain their state
        """
        manager = RegistryManager()
        registry = manager.create_registry("test_registry")

        # Use the registry via the manager
        retrieved_registry = manager.get_registry("test_registry")
        retrieved_registry.add("key1", "value1")
        retrieved_registry.add("key2", "value2")

        # Verify that the changes are persistent
        assert len(registry) == 2
        assert registry.get("key1") == "value1"
        assert registry.get("key2") == "value2"

        # Verify via the manager
        assert len(manager.get_registry("test_registry")) == 2
        assert manager.get_registry("test_registry").get("key1") == "value1"

    def test_manager_with_empty_registry_names(self) -> None:
        """
        Scenario: Creation of registries with empty or special names

        Expected:
        - The registries are created with the given names
        - The registries are accessible with these names
        - The names are preserved exactly
        """
        manager = RegistryManager()

        # Test with empty name
        empty_registry = manager.create_registry("")
        assert empty_registry.name == ""
        assert manager.get_registry("") is empty_registry

        # Test with name containing spaces
        space_registry = manager.create_registry("test registry")
        assert space_registry.name == "test registry"
        assert manager.get_registry("test registry") is space_registry

        # Test with name containing special characters
        special_registry = manager.create_registry("test-registry_123")
        assert special_registry.name == "test-registry_123"
        assert manager.get_registry("test-registry_123") is special_registry

    def test_manager_registry_lifecycle(self) -> None:
        """
        Scenario: Complete lifecycle of a registry via the manager

        Expected:
        - The registry can be created, used, and retrieved
        - The registry maintains its state between retrievals
        - The registry can be used for complex operations
        """
        manager = RegistryManager()

        # Create the registry
        registry = manager.create_registry("lifecycle_test")

        # Use the registry
        registry.add("key1", "value1")
        registry.add("key2", "value2")

        # Retrieve the registry and verify the state
        retrieved_registry = manager.get_registry("lifecycle_test")
        assert len(retrieved_registry) == 2
        assert retrieved_registry.get("key1") == "value1"
        assert retrieved_registry.get("key2") == "value2"

        # Modify the registry via the retrieval
        retrieved_registry.add("key3", "value3")
        retrieved_registry.unregister("key1")

        # Verify that the changes are persistent
        assert len(registry) == 2
        assert "key1" not in registry
        assert "key2" in registry
        assert "key3" in registry
        assert registry.get("key2") == "value2"
        assert registry.get("key3") == "value3"
