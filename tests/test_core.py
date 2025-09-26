"""
Tests unitaires for the core.py module - Registry class.
"""

# mypy: ignore-errors

import pytest

from regman.core import Registry


class TestRegistry:
    """Tests for the Registry class."""

    def test_init(self) -> None:
        """
        Scenario: Initialization of a new registry

        Expected:
        - The name of the registry is correctly defined
        - The registry is empty
        - The lock is initialized
        """
        registry = Registry("test_registry")
        assert registry.name == "test_registry"
        assert len(registry) == 0
        assert registry.keys() == []
        assert registry.list() == {}

    def test_register_decorator_without_key(self) -> None:
        """
        Scenario: Registration of an object with the decorator without explicit key

        Expected:
        - The object is registered with its class name as key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @registry.register()
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass
        assert "TestClass" in registry.keys()
        assert registry.list()["TestClass"] is TestClass

    def test_register_decorator_with_key(self) -> None:
        """
        Scenario: Registration of an object with the decorator with explicit key

        Expected:
        - The object is registered with the provided key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @registry.register("custom_key")
        class TestClass:
            pass

        assert "custom_key" in registry
        assert registry.get("custom_key") is TestClass
        assert "custom_key" in registry.keys()
        assert registry.list()["custom_key"] is TestClass

    def test_register_decorator_with_function(self) -> None:
        """
        Scenario: Registration of a function with the decorator

        Expected:
        - The function is registered with its name as key
        - The function is accessible via get()
        - The function appears in keys() and list()
        """
        registry = Registry("test_registry")

        @registry.register()
        def test_function() -> str:
            return "test"

        assert "test_function" in registry
        assert registry.get("test_function") is test_function
        assert "test_function" in registry.keys()
        assert registry.list()["test_function"] is test_function

    def test_add_method(self) -> None:
        """
        Scenario: Explicit addition of an object with the add() method

        Expected:
        - The object is registered with the provided key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")
        test_obj = "test_object"

        registry.add("test_key", test_obj)

        assert "test_key" in registry
        assert registry.get("test_key") is test_obj
        assert "test_key" in registry.keys()
        assert registry.list()["test_key"] is test_obj

    def test_register_duplicate_key_raises_error(self) -> None:
        """
        Scenario: Attempt to register a duplicate key

        Expected:
        - A ValueError is raised
        - The error message contains the registry name and the key
        """
        registry = Registry("test_registry")
        registry.add("duplicate_key", "first_object")

        with pytest.raises(
            ValueError, match="test_registry: 'duplicate_key' already registered."
        ):
            registry.add("duplicate_key", "second_object")

    def test_get_nonexistent_key_raises_keyerror(self) -> None:
        """
        Scenario: Attempt to get a nonexistent key

        Expected:
        - A KeyError is raised
        """
        registry = Registry("test_registry")

        with pytest.raises(KeyError):
            registry.get("nonexistent_key")

    def test_unregister_existing_key(self) -> None:
        """
        Scenario: Deletion of an existing key

        Expected:
        - The key is removed from the registry
        - The key no longer appears in keys() and list()
        - len() returns 0
        """
        registry = Registry("test_registry")
        registry.add("test_key", "test_object")

        assert "test_key" in registry
        assert len(registry) == 1

        registry.unregister("test_key")

        assert "test_key" not in registry
        assert len(registry) == 0
        assert "test_key" not in registry.keys()
        assert "test_key" not in registry.list()

    def test_unregister_nonexistent_key_no_error(self) -> None:
        """
        Scenario: Deletion of a nonexistent key

        Expected:
        - No error is raised
        - The registry remains unchanged
        """
        registry = Registry("test_registry")
        initial_size = len(registry)

        registry.unregister("nonexistent_key")

        assert len(registry) == initial_size

    def test_clear_registry(self) -> None:
        """
        Scenario: Complete clearing of the registry

        Expected:
        - All keys are removed
        - The registry is empty
        - len() returns 0
        """
        registry = Registry("test_registry")
        registry.add("key1", "obj1")
        registry.add("key2", "obj2")
        registry.add("key3", "obj3")

        assert len(registry) == 3

        registry.clear()

        assert len(registry) == 0
        assert registry.keys() == []
        assert registry.list() == {}

    def test_contains_operator(self) -> None:
        """
        Scenario: Usage of the 'in' operator to check the presence of a key

        Expected:
        - 'in' returns True for existing keys
        - 'in' returns False for nonexistent keys
        """
        registry = Registry("test_registry")
        registry.add("existing_key", "test_object")

        assert "existing_key" in registry
        assert "nonexistent_key" not in registry

    def test_len_operator(self) -> None:
        """
        Scenario: Usage of the len() operator to get the size of the registry

        Expected:
        - len() returns the correct number of elements
        - len() changes after adding/deleting elements
        """
        registry = Registry("test_registry")

        assert len(registry) == 0

        registry.add("key1", "obj1")
        assert len(registry) == 1

        registry.add("key2", "obj2")
        assert len(registry) == 2

        registry.unregister("key1")
        assert len(registry) == 1

    def test_repr(self) -> None:
        """
        Scenario: String representation of the registry

        Expected:
        - The representation contains the name and size of the registry
        - The representation changes with the size
        """
        registry = Registry("test_registry")
        assert repr(registry) == "<Registry name=test_registry size=0>"

        registry.add("key1", "obj1")
        assert repr(registry) == "<Registry name=test_registry size=1>"

    def test_keys_returns_copy(self) -> None:
        """
        Scenario: Modification of the list returned by keys() does not modify the registry

        Expected:
        - keys() returns a copy of the list
        - Modification of the list returned does not affect the registry
        """
        registry = Registry("test_registry")
        registry.add("key1", "obj1")
        registry.add("key2", "obj2")

        keys = registry.keys()
        keys.append("key3")

        assert len(registry) == 2
        assert "key3" not in registry

    def test_list_returns_copy(self) -> None:
        """
        Scenario: Modification of the dictionary returned by list() does not modify the registry

        Expected:
        - list() returns a copy of the dictionary
        - Modification of the dictionary returned does not affect the registry
        """
        registry = Registry("test_registry")
        registry.add("key1", "obj1")

        registry_dict = registry.list()
        registry_dict["key2"] = "obj2"

        assert len(registry) == 1
        assert "key2" not in registry

    def test_multiple_registries_independence(self) -> None:
        """
        Scenario: Usage of multiple registries simultaneously

        Expected:
        - The registries are independent
        - The keys of a registry do not affect the others
        """
        registry1 = Registry("registry1")
        registry2 = Registry("registry2")

        registry1.add("key1", "obj1")
        registry2.add("key1", "obj2")

        assert registry1.get("key1") == "obj1"
        assert registry2.get("key1") == "obj2"
        assert len(registry1) == 1
        assert len(registry2) == 1

    def test_register_with_none_key_uses_obj_name(self) -> None:
        """
        Scenario: Registration with None key uses the name of the object

        Expected:
        - The key used is the name of the object
        - The object is accessible with this key
        """
        registry = Registry("test_registry")

        @registry.register(None)
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass

    def test_register_with_empty_string_key_uses_obj_name(self) -> None:
        """
        Scenario: Registration with empty string key uses the name of the object

        Expected:
        - The key used is the name of the object
        - The object is accessible with this key
        """
        registry = Registry("test_registry")

        @registry.register("")
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass
