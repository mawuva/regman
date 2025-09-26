"""
Tests unitaires for the decorators.py module.
"""

# mypy: ignore-errors

import pytest

from regman.core import Registry
from regman.decorators import register


class TestRegisterDecorator:
    """Tests for the register decorator."""

    def test_register_decorator_without_key(self) -> None:
        """
        Scenario: Usage of the register decorator without an explicit key

        Expected:
        - The object is registered with its name as key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry)
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass
        assert "TestClass" in registry.keys()
        assert registry.list()["TestClass"] is TestClass

    def test_register_decorator_with_key(self) -> None:
        """
        Scenario: Usage of the register decorator with an explicit key

        Expected:
        - The object is registered with the provided key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry, "custom_key")
        class TestClass:
            pass

        assert "custom_key" in registry
        assert registry.get("custom_key") is TestClass
        assert "custom_key" in registry.keys()
        assert registry.list()["custom_key"] is TestClass

    def test_register_decorator_with_function(self) -> None:
        """
        Scenario: Usage of the register decorator with a function object

        Expected:
        - The function is registered with its name as key
        - The function is accessible via get()
        - The function appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry)
        def test_function() -> str:
            return "test"

        assert "test_function" in registry
        assert registry.get("test_function") is test_function
        assert "test_function" in registry.keys()
        assert registry.list()["test_function"] is test_function

    def test_register_decorator_with_method(self) -> None:
        """
        Scenario: Usage of the register decorator with a method

        Expected:
        - The method is registered with its name as key
        - The method is accessible via get()
        - The method appears in keys() and list()
        """
        registry = Registry("test_registry")

        class TestClass:
            @register(registry)
            def test_method(self) -> str:
                return "test"

        assert "test_method" in registry
        assert registry.get("test_method") is TestClass.test_method
        assert "test_method" in registry.keys()
        assert registry.list()["test_method"] is TestClass.test_method

    def test_register_decorator_with_lambda(self) -> None:
        """
        Scenario: Usage of the register decorator with a lambda

        Expected:
        - The lambda is registered with the provided key
        - The lambda is accessible via get()
        - The lambda appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry, "lambda_func")
        def lambda_func() -> str:
            return "lambda"

        assert "lambda_func" in registry
        assert registry.get("lambda_func") is lambda_func
        assert "lambda_func" in registry.keys()
        assert registry.list()["lambda_func"] is lambda_func

    def test_register_decorator_with_none_key_uses_obj_name(self) -> None:
        """
        Scenario: Usage of the register decorator with None key

        Expected:
        - The object is registered with its name as key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry, None)
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass
        assert "TestClass" in registry.keys()
        assert registry.list()["TestClass"] is TestClass

    def test_register_decorator_with_empty_string_key_uses_obj_name(self) -> None:
        """
        Scenario: Usage of the register decorator with empty string key

        Expected:
        - The object is registered with its name as key
        - The object is accessible via get()
        - The object appears in keys() and list()
        """
        registry = Registry("test_registry")

        @register(registry, "")
        class TestClass:
            pass

        assert "TestClass" in registry
        assert registry.get("TestClass") is TestClass
        assert "TestClass" in registry.keys()
        assert registry.list()["TestClass"] is TestClass

    def test_register_decorator_returns_original_object(self) -> None:
        """
        Scenario: The register decorator returns the original object

        Expected:
        - The decorator returns the original object without modification
        - The object can be used normally after registration
        """
        registry = Registry("test_registry")

        @register(registry)
        def test_function() -> str:
            return "test"

        # Verify that the function still works
        assert test_function() == "test"
        assert callable(test_function)

    def test_register_decorator_with_multiple_objects(self) -> None:
        """
        Scenario: Usage of the register decorator with multiple objects

        Expected:
        - All objects are registered correctly
        - Each object is accessible with its respective key
        - The registry contains all objects
        """
        registry = Registry("test_registry")

        @register(registry, "class1")
        class TestClass1:
            pass

        @register(registry, "class2")
        class TestClass2:
            pass

        @register(registry)
        def test_function() -> str:
            return "test"

        assert len(registry) == 3
        assert "class1" in registry
        assert "class2" in registry
        assert "test_function" in registry
        assert registry.get("class1") is TestClass1
        assert registry.get("class2") is TestClass2
        assert registry.get("test_function") is test_function

    def test_register_decorator_with_different_registries(self) -> None:
        """
        Scenario: Usage of the register decorator with different registries

        Expected:
        - The objects are registered in the correct registry
        - The registries are independent
        - Each object appears only in its registry
        """
        registry1 = Registry("registry1")
        registry2 = Registry("registry2")

        @register(registry1, "test")
        class TestClass1:
            pass

        @register(registry2, "test")
        class TestClass2:
            pass

        assert "test" in registry1
        assert "test" in registry2
        assert registry1.get("test") is TestClass1
        assert registry2.get("test") is TestClass2
        assert len(registry1) == 1
        assert len(registry2) == 1

    def test_register_decorator_with_duplicate_key_raises_error(self) -> None:
        """
        Scenario: Attempt to register with an already existing key

        Expected:
        - A ValueError is raised
        - The error message contains the name of the registry and the key
        """
        registry = Registry("test_registry")

        @register(registry, "duplicate_key")
        class TestClass1:
            pass

        with pytest.raises(
            ValueError, match="test_registry: 'duplicate_key' already registered."
        ):

            @register(registry, "duplicate_key")
            class TestClass2:
                pass

    def test_register_decorator_with_complex_object(self) -> None:
        """
        Scenario: Usage of the register decorator with a complex object

        Expected:
        - The complex object is registered correctly
        - The object is accessible via get()
        - The object retains its properties
        """
        registry = Registry("test_registry")

        class ComplexClass:
            def __init__(self, value: str) -> None:
                self.value = value

            def method(self) -> str:
                return self.value

        @register(registry, "complex")
        def create_complex() -> ComplexClass:
            return ComplexClass("test_value")

        assert "complex" in registry
        assert registry.get("complex") is create_complex

        # Verify that the function still works
        obj = create_complex()
        assert obj.value == "test_value"
        assert obj.method() == "test_value"

    def test_register_decorator_preserves_object_metadata(self) -> None:
        """
        Scenario: The register decorator preserves the object's metadata

        Expected:
        - The object retains its name, docstring, and other attributes
        - The object can be inspected normally
        """
        registry = Registry("test_registry")

        @register(registry)
        def documented_function() -> str:
            """This is a documented function."""
            return "test"

        assert documented_function.__name__ == "documented_function"
        assert documented_function.__doc__ == "This is a documented function."
        assert callable(documented_function)
