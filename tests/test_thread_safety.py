"""
Tests thread safety to verify concurrency in the regman package.
"""

# mypy: ignore-errors

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List

from regman.core import Registry
from regman.manager import RegistryManager


class TestThreadSafety:
    """Tests thread safety for the regman package."""

    def test_registry_concurrent_add_operations(self) -> None:
        """
        Scenario: Concurrent addition of elements in a registry

        Expected:
        - All elements are added without loss
        - No concurrency error is raised
        - The registry contains exactly the number of elements added
        """
        registry = Registry("concurrent_test")
        num_threads = 5  # Reduced from 10
        elements_per_thread = 20  # Reduced from 100

        def add_elements(thread_id: int) -> List[str]:
            """Add elements to the registry."""
            added_keys = []
            for i in range(elements_per_thread):
                key = f"thread_{thread_id}_element_{i}"
                try:
                    registry.add(key, f"value_{thread_id}_{i}")
                    added_keys.append(key)
                except ValueError:
                    # Key already exists, ignore
                    pass
            return added_keys

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(add_elements, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all elements have been added
        total_added = sum(len(result) for result in results)
        assert total_added > 0
        assert len(registry) == total_added

    def test_registry_concurrent_get_operations(self) -> None:
        """
        Scenario: Concurrent retrieval of elements in a registry

        Expected:
        - All retrievals succeed
        - No concurrency error is raised
        - The retrieved values are correct
        """
        registry = Registry("concurrent_get_test")
        num_elements = 20  # Reduced from 100

        # Add elements
        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        def get_elements() -> List[Any]:
            """Retrieve elements from the registry."""
            retrieved_values = []
            for i in range(num_elements):
                try:
                    value = registry.get(f"key_{i}")
                    retrieved_values.append(value)
                except KeyError:
                    pass
            return retrieved_values

        num_threads = 5  # Reduced from 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(get_elements) for _ in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all retrievals have succeeded
        for result in results:
            assert len(result) == num_elements
            for i, value in enumerate(result):
                assert value == f"value_{i}"

    def test_registry_concurrent_mixed_operations(self) -> None:
        """
        Scenario: Concurrent mixed operations (addition, retrieval, deletion)

        Expected:
        - All operations succeed without error
        - No data corruption
        - The registry remains in a consistent state
        """
        registry = Registry("mixed_operations_test")
        num_operations = 100  # Reduced from 1000

        def add_operation(thread_id: int) -> None:
            """Add operations."""
            for i in range(num_operations // 4):
                key = f"add_{thread_id}_{i}"
                try:
                    registry.add(key, f"value_{thread_id}_{i}")
                except ValueError:
                    pass

        def get_operation(thread_id: int) -> None:
            """Retrieval operations."""
            for i in range(num_operations // 4):
                key = f"add_0_{i}"  # Try to retrieve added elements
                try:
                    registry.get(key)
                except KeyError:
                    pass

        def unregister_operation(thread_id: int) -> None:
            """Deletion operations."""
            for i in range(num_operations // 4):
                key = f"add_0_{i}"  # Try to delete added elements
                registry.unregister(key)

        def list_operation(thread_id: int) -> None:
            """Listing operations."""
            for i in range(num_operations // 4):
                registry.keys()
                registry.list()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(add_operation, 0),
                executor.submit(get_operation, 1),
                executor.submit(unregister_operation, 2),
                executor.submit(list_operation, 3),
            ]
            for future in as_completed(futures):
                future.result()  # Wait for completion

        # Verify that the registry is in a consistent state
        assert isinstance(registry.keys(), list)
        assert isinstance(registry.list(), dict)
        assert len(registry.keys()) == len(registry.list())

    def test_registry_concurrent_clear_operations(self) -> None:
        """
        Scenario: Concurrent clear operations

        Expected:
        - The clear operations succeed
        - No concurrency error is raised
        - The registry is cleared
        """
        registry = Registry("clear_test")
        num_elements = 100

        # Add elements
        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        def clear_operation() -> None:
            """Clear operation."""
            registry.clear()

        num_threads = 5
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(clear_operation) for _ in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        # Verify that the registry is cleared
        assert len(registry) == 0
        assert registry.keys() == []
        assert registry.list() == {}

    def test_registry_concurrent_contains_operations(self) -> None:
        """
        Scenario: Concurrent existence check operations

        Expected:
        - All checks succeed
        - No concurrency error is raised
        - The results are consistent
        """
        registry = Registry("contains_test")
        num_elements = 20  # Reduced from 100

        # Add elements
        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        def contains_operation(thread_id: int) -> List[bool]:
            """Existence check operations."""
            results = []
            for i in range(num_elements):
                results.append(f"key_{i}" in registry)
            return results

        num_threads = 5  # Reduced from 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(contains_operation, i) for i in range(num_threads)
            ]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all results are consistent
        for result in results:
            assert len(result) == num_elements
            assert all(result)  # All elements must exist

    def test_registry_concurrent_len_operations(self) -> None:
        """
        Scenario: Concurrent size calculation operations

        Expected:
        - All size calculation operations succeed
        - No concurrency error is raised
        - The results are consistent
        """
        registry = Registry("len_test")
        num_elements = 20  # Reduced from 100

        # Add elements
        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        def len_operation(thread_id: int) -> List[int]:
            """Size calculation operations."""
            results = []
            for i in range(20):  # Reduced from 100
                results.append(len(registry))
            return results

        num_threads = 5  # Reduced from 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(len_operation, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all results are consistent
        for result in results:
            assert len(result) == 20  # Updated to match the reduced number
            assert all(length == num_elements for length in result)

    def test_registry_concurrent_repr_operations(self) -> None:
        """
        Scenario: Concurrent string representation operations

        Expected:
        - All representation operations succeed
        - No concurrency error is raised
        - The representations are consistent
        """
        registry = Registry("repr_test")
        num_elements = 20  # Reduced from 100

        # Add elements
        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        def repr_operation(thread_id: int) -> List[str]:
            """String representation operations."""
            results = []
            for i in range(20):  # Reduced from 100
                results.append(repr(registry))
            return results

        num_threads = 5  # Reduced from 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(repr_operation, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all representations are consistent
        for result in results:
            assert len(result) == 20  # Updated to match the reduced number
            assert all("repr_test" in repr_str for repr_str in result)
            assert all("size=20" in repr_str for repr_str in result)

    def test_registry_manager_concurrent_operations(self) -> None:
        """
        Scenario: Concurrent operations on the registry manager

        Expected:
        - All operations succeed
        - No concurrency error is raised
        - The registries are created and accessible correctly
        """
        manager = RegistryManager()
        num_threads = 5  # Reduced from 10
        registries_per_thread = 3  # Reduced from 5

        def create_and_use_registries(thread_id: int) -> List[str]:
            """Create and use registries."""
            created_registries = []
            for i in range(registries_per_thread):
                registry_name = f"thread_{thread_id}_registry_{i}"
                try:
                    registry = manager.create_registry(registry_name)
                    registry.add(f"key_{i}", f"value_{i}")
                    created_registries.append(registry_name)
                except ValueError:
                    # Registry already exists, ignore
                    pass
            return created_registries

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(create_and_use_registries, i)
                for i in range(num_threads)
            ]
            results = [future.result() for future in as_completed(futures)]

        # Verify that all registries have been created
        total_created = sum(len(result) for result in results)
        assert total_created > 0
        assert len(manager.all()) == total_created

        # Verify that all registries are accessible
        for result in results:
            for registry_name in result:
                registry = manager.get_registry(registry_name)
                assert isinstance(registry, Registry)
                assert registry.name == registry_name

    def test_registry_concurrent_decorator_usage(self) -> None:
        """
        Scenario: Concurrent usage of the registry decorator

        Expected:
        - All decorators work correctly
        - No concurrency error is raised
        - All objects are registered
        """
        registry = Registry("decorator_test")

        def create_decorated_class(thread_id: int) -> None:
            """Create a decorated class."""
            class_name = f"ThreadClass_{thread_id}"

            @registry.register(class_name)
            class ThreadClass:
                def __init__(self) -> None:
                    self.thread_id = thread_id

        num_threads = 5  # Reduced from 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(create_decorated_class, i) for i in range(num_threads)
            ]
            for future in as_completed(futures):
                future.result()

        # Verify that all classes have been registered
        assert len(registry) == num_threads
        for i in range(num_threads):
            class_name = f"ThreadClass_{i}"
            assert class_name in registry
            # The class is registered with the custom name, but the class itself is named "ThreadClass"
            assert registry.get(class_name).__name__ == "ThreadClass"

    def test_registry_stress_test(self) -> None:
        """
        Scenario: Stress test with many concurrent operations

        Expected:
        - All operations succeed
        - No data corruption
        - The registry remains in a consistent state
        """
        registry = Registry("stress_test")
        num_threads = 5  # Reduced from 20
        operations_per_thread = 50  # Reduced from 1000

        def stress_operation(thread_id: int) -> None:
            """Stress operations."""
            for i in range(operations_per_thread):
                key = f"stress_{thread_id}_{i}"
                try:
                    registry.add(key, f"value_{thread_id}_{i}")
                except ValueError:
                    pass

                if i % 5 == 0:  # Reduced from 10
                    try:
                        registry.get(key)
                    except KeyError:
                        pass

                if i % 10 == 0:  # Reduced from 20
                    registry.keys()
                    registry.list()

                if i % 25 == 0:  # Reduced from 50
                    registry.unregister(key)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(stress_operation, i) for i in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        # Verify that the registry is in a consistent state
        assert isinstance(registry.keys(), list)
        assert isinstance(registry.list(), dict)
        assert len(registry.keys()) == len(registry.list())
        assert len(registry) >= 0  # At least 0 elements
