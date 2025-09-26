"""
Tests for error cases and exceptions in the regman package.
"""

# mypy: ignore-errors

import pytest

from regman.core import Registry
from regman.decorators import register
from regman.manager import RegistryManager

# Constants for special characters and Unicode tests
SPECIAL_CHARACTERS = [
    "key-with-dash",
    "key_with_underscore",
    "key.with.dots",
    "key@with#symbols",
    "key/with/slashes",
    "key\\with\\backslashes",
    "key:with:colons",
    "key;with;semicolons",
    "key,with,commas",
    "key|with|pipes",
    "key&with&ampersands",
    "key%with%percent",
    "key+with+plus",
    "key=with=equals",
    "key?with?question",
    "key!with!exclamation",
    "key<with>angles",
    "key[with]brackets",
    "key{with}braces",
    "key(with)parentheses",
]

UNICODE_CHARACTERS = [
    "clé_avec_accents",
    "ключ_на_русском",
    "鍵_中文",
    "🔑_emoji",
    "key_ñ_español",
    "key_ä_ö_ü_german",
    "key_é_français",
    "key_日本語",
    "key_한국어",
    "key_العربية",
]

# Variants for registry names
SPECIAL_REGISTRY_NAMES = [
    name.replace("key", "registry") for name in SPECIAL_CHARACTERS
]
UNICODE_REGISTRY_NAMES = [
    "registre_avec_accents",
    "регистр_на_русском",
    "註冊表_中文",
    "📋_emoji",
    "registro_ñ_español",
    "registrierung_ä_ö_ü_german",
    "registre_é_français",
    "登録_日本語",
    "등록_한국어",
    "تسجيل_العربية",
]


class TestErrorCases:
    """Tests for error cases and exceptions."""

    def test_registry_duplicate_key_error(self) -> None:
        """
        Scenario: Attempt to add a duplicate key

        Expected:
        - A ValueError is raised
        - The error message contains the registry name and the key
        - The registry remains unchanged
        """
        registry = Registry("error_test")
        registry.add("duplicate_key", "first_value")

        with pytest.raises(
            ValueError, match="error_test: 'duplicate_key' already registered."
        ):
            registry.add("duplicate_key", "second_value")

        # Verify that the registry has not changed
        assert len(registry) == 1
        assert registry.get("duplicate_key") == "first_value"

    def test_registry_keyerror_on_nonexistent_key(self) -> None:
        """
        Scenario: Attempt to retrieve a nonexistent key

        Expected:
        - A KeyError is raised
        - The error message contains the key
        """
        registry = Registry("error_test")

        with pytest.raises(KeyError):
            registry.get("nonexistent_key")

    def test_registry_keyerror_on_empty_registry(self) -> None:
        """
        Scenario: Attempt to retrieve from an empty registry

        Expected:
        - A KeyError is raised
        """
        registry = Registry("empty_test")

        with pytest.raises(KeyError):
            registry.get("any_key")

    def test_registry_manager_duplicate_registry_error(self) -> None:
        """
        Scenario: Attempt to create a registry with a duplicate name

        Expected:
        - A ValueError is raised
        - The error message contains the registry name
        - The manager remains unchanged
        """
        manager = RegistryManager()
        manager.create_registry("duplicate_name")

        with pytest.raises(
            ValueError, match="Registry 'duplicate_name' already exists."
        ):
            manager.create_registry("duplicate_name")

        # Verify that the manager has only one registry
        assert len(manager.all()) == 1
        assert "duplicate_name" in manager.all()

    def test_registry_manager_keyerror_on_nonexistent_registry(self) -> None:
        """
        Scenario: Attempt to retrieve a nonexistent registry

        Expected:
        - A KeyError is raised
        """
        manager = RegistryManager()

        with pytest.raises(KeyError):
            manager.get_registry("nonexistent_registry")

    def test_registry_manager_keyerror_on_empty_manager(self) -> None:
        """
        Scenario: Attempt to retrieve from an empty manager

        Expected:
        - A KeyError is raised
        """
        manager = RegistryManager()

        with pytest.raises(KeyError):
            manager.get_registry("any_registry")

    def test_registry_invalid_key_types(self) -> None:
        """
        Scenario: Usage of invalid key types

        Expected:
        - Unhashable types raise TypeError
        - Hashable non-string types are accepted (Python behavior)
        """
        registry = Registry("type_test")

        # Test with unhashable types (should raise TypeError)
        unhashable_keys = [[], {}, set()]

        for invalid_key in unhashable_keys:
            with pytest.raises(TypeError, match="unhashable type"):
                registry.add(invalid_key, "value")

            with pytest.raises(TypeError, match="unhashable type"):
                registry.get(invalid_key)

            # unregister with pop(key, None) doesn't raise TypeError for unhashable types
            # It just returns None silently
            registry.unregister(invalid_key)  # Should not raise exception

            with pytest.raises(TypeError, match="unhashable type"):
                invalid_key in registry

    def test_registry_non_string_hashable_keys(self) -> None:
        """
        Scenario: Usage of non-string but hashable key types

        Expected:
        - Hashable non-string types are accepted (Python behavior)
        - Operations work normally with these types
        """
        registry = Registry("hashable_test")

        # Test with hashable non-string types (should work)
        hashable_keys = [None, 123, tuple(), frozenset()]

        for key in hashable_keys:
            registry.add(key, f"value_{key}")
            assert key in registry
            assert registry.get(key) == f"value_{key}"

        assert len(registry) == len(hashable_keys)

    def test_registry_empty_string_key(self) -> None:
        """
        Scenario: Usage of empty keys

        Expected:
        - Empty keys are accepted
        - The operations function normally
        """
        registry = Registry("empty_key_test")

        # Test with empty key
        registry.add("", "empty_key_value")
        assert "" in registry
        assert registry.get("") == "empty_key_value"
        assert len(registry) == 1

        # Test with deletion
        registry.unregister("")
        assert "" not in registry
        assert len(registry) == 0

    def test_registry_whitespace_keys(self) -> None:
        """
        Scenario: Usage of keys with spaces

        Expected:
        - Keys with spaces are accepted
        - The operations function normally
        """
        registry = Registry("whitespace_test")

        # Test with different types of spaces
        whitespace_keys = [" ", "  ", "\t", "\n", " \t\n "]

        for key in whitespace_keys:
            registry.add(key, f"value_{key}")
            assert key in registry
            assert registry.get(key) == f"value_{key}"

        assert len(registry) == len(whitespace_keys)

    def test_registry_special_character_keys(self) -> None:
        """
        Scenario: Usage of keys with special characters

        Expected:
        - Keys with special characters are accepted
        - The operations function normally
        """
        registry = Registry("special_chars_test")

        for key in SPECIAL_CHARACTERS:
            registry.add(key, f"value_{key}")
            assert key in registry
            assert registry.get(key) == f"value_{key}"

        assert len(registry) == len(SPECIAL_CHARACTERS)

    def test_registry_unicode_keys(self) -> None:
        """
        Scenario: Usage of keys with Unicode characters

        Expected:
        - Unicode keys are accepted
        - The operations function normally
        """
        registry = Registry("unicode_test")

        for key in UNICODE_CHARACTERS:
            registry.add(key, f"value_{key}")
            assert key in registry
            assert registry.get(key) == f"value_{key}"

        assert len(registry) == len(UNICODE_CHARACTERS)

    def test_registry_very_long_keys(self) -> None:
        """
        Scenario: Usage of very long keys

        Expected:
        - Very long keys are accepted
        - The operations function normally
        """
        registry = Registry("long_key_test")

        # Test with keys of different lengths
        long_keys = [
            "a" * 1000,
            "b" * 10000,
            "c" * 100000,
        ]

        for key in long_keys:
            registry.add(key, f"value_{len(key)}")
            assert key in registry
            assert registry.get(key) == f"value_{len(key)}"

        assert len(registry) == len(long_keys)

    def test_registry_none_values(self) -> None:
        """
        Scenario: Usage of None values

        Expected:
        - None values are accepted
        - The operations function normally
        """
        registry = Registry("none_value_test")

        registry.add("none_key", None)
        assert "none_key" in registry
        assert registry.get("none_key") is None
        assert len(registry) == 1

    def test_registry_complex_values(self) -> None:
        """
        Scenario: Usage of complex values

        Expected:
        - Complex values are accepted
        - The operations function normally
        """
        registry = Registry("complex_value_test")

        # Test with different types of complex values
        complex_values = [
            [1, 2, 3],
            {"a": 1, "b": 2},
            {1, 2, 3},
            (1, 2, 3),
            lambda x: x * 2,
            object(),
        ]

        for i, value in enumerate(complex_values):
            key = f"complex_key_{i}"
            registry.add(key, value)
            assert key in registry
            assert registry.get(key) is value

        assert len(registry) == len(complex_values)

    def test_registry_decorator_with_invalid_registry(self) -> None:
        """
        Scenario: Usage of the decorator with an invalid registry

        Expected:
        - An appropriate error is raised
        """
        with pytest.raises((TypeError, AttributeError)):

            @register(None)  # type: ignore
            class TestClass:
                pass

    def test_registry_decorator_with_invalid_key_type(self) -> None:
        """
        Scenario: Usage of the decorator with an invalid key type

        Expected:
        - The decorator works with non-string types (Python behavior)
        - The object is registered with the non-string key
        """
        registry = Registry("decorator_error_test")

        @register(registry, 123)  # type: ignore
        class TestClass:
            pass

        # The decorator should work with non-string keys
        assert 123 in registry
        assert registry.get(123) is TestClass

    def test_registry_manager_invalid_registry_name_types(self) -> None:
        """
        Scenario: Usage of invalid registry name types

        Expected:
        - Unhashable types raise TypeError
        - Hashable non-string types are accepted (Python behavior)
        """
        manager = RegistryManager()

        # Test with unhashable types (should raise TypeError)
        unhashable_names = [[], {}, set()]

        for invalid_name in unhashable_names:
            with pytest.raises(TypeError, match="unhashable type"):
                manager.create_registry(invalid_name)  # type: ignore

            with pytest.raises(TypeError, match="unhashable type"):
                manager.get_registry(invalid_name)  # type: ignore

    def test_registry_manager_non_string_hashable_names(self) -> None:
        """
        Scenario: Usage of non-string but hashable registry name types

        Expected:
        - Hashable non-string types are accepted (Python behavior)
        - Operations work normally with these types
        """
        manager = RegistryManager()

        # Test with hashable non-string types (should work)
        hashable_names = [None, 123, tuple(), frozenset()]

        for name in hashable_names:
            registry = manager.create_registry(name)  # type: ignore
            assert registry.name == name
            assert manager.get_registry(name) is registry  # type: ignore

        assert len(manager.all()) == len(hashable_names)

    def test_registry_manager_empty_registry_name(self) -> None:
        """
        Scenario: Usage of empty registry names

        Expected:
        - Empty names are accepted
        - The operations function normally
        """
        manager = RegistryManager()

        # Test with empty name
        registry = manager.create_registry("")
        assert registry.name == ""
        assert manager.get_registry("") is registry
        assert len(manager.all()) == 1

    def test_registry_manager_whitespace_registry_names(self) -> None:
        """
        Scenario: Usage of registry names with spaces

        Expected:
        - Names with spaces are accepted
        - The operations function normally
        """
        manager = RegistryManager()

        # Test with different types of spaces
        whitespace_names = [" ", "  ", "\t", "\n", " \t\n "]

        for name in whitespace_names:
            registry = manager.create_registry(name)
            assert registry.name == name
            assert manager.get_registry(name) is registry

        assert len(manager.all()) == len(whitespace_names)

    def test_registry_manager_special_character_registry_names(self) -> None:
        """
        Scenario: Usage of registry names with special characters

        Expected:
        - Names with special characters are accepted
        - The operations function normally
        """
        manager = RegistryManager()

        for name in SPECIAL_REGISTRY_NAMES:
            registry = manager.create_registry(name)
            assert registry.name == name
            assert manager.get_registry(name) is registry

        assert len(manager.all()) == len(SPECIAL_REGISTRY_NAMES)

    def test_registry_manager_unicode_registry_names(self) -> None:
        """
        Scenario: Usage of registry names with Unicode characters

        Expected:
        - Unicode names are accepted
        - The operations function normally
        """
        manager = RegistryManager()

        for name in UNICODE_REGISTRY_NAMES:
            registry = manager.create_registry(name)
            assert registry.name == name
            assert manager.get_registry(name) is registry

        assert len(manager.all()) == len(UNICODE_REGISTRY_NAMES)

    def test_registry_manager_very_long_registry_names(self) -> None:
        """
        Scenario: Usage of very long registry names

        Expected:
        - Very long names are accepted
        - The operations function normally
        """
        manager = RegistryManager()

        # Test with names of different lengths
        long_names = [
            "a" * 1000,
            "b" * 10000,
            "c" * 100000,
        ]

        for name in long_names:
            registry = manager.create_registry(name)
            assert registry.name == name
            assert manager.get_registry(name) is registry

        assert len(manager.all()) == len(long_names)

    def test_registry_edge_case_empty_registry_operations(self) -> None:
        """
        Scenario: Operations on an empty registry

        Expected:
        - The operations of deletion and retrieval fail
        - The operations of listing and size function normally
        """
        registry = Registry("empty_edge_test")

        # Test with operations on an empty registry
        assert len(registry) == 0
        assert registry.keys() == []
        assert registry.list() == {}
        assert "any_key" not in registry

        # Test with deletion of a nonexistent key (should not raise an error)
        registry.unregister("nonexistent_key")
        assert len(registry) == 0

        # Test with retrieval of a nonexistent key (should raise an error)
        with pytest.raises(KeyError):
            registry.get("nonexistent_key")

    def test_registry_edge_case_single_element_operations(self) -> None:
        """
        Scenario: Operations on a registry with a single element

        Expected:
        - All operations function correctly
        - The registry remains consistent
        """
        registry = Registry("single_element_test")
        registry.add("single_key", "single_value")

        # Test with basic operations
        assert len(registry) == 1
        assert "single_key" in registry
        assert registry.get("single_key") == "single_value"
        assert registry.keys() == ["single_key"]
        assert registry.list() == {"single_key": "single_value"}

        # Test with deletion
        registry.unregister("single_key")
        assert len(registry) == 0
        assert "single_key" not in registry

        # Test with retrieval after deletion
        with pytest.raises(KeyError):
            registry.get("single_key")
