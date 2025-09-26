# mypy: ignore-errors

"""
Concurrent usage example of regman.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Any

from regman import Registry, register, RegistryManager


class TaskProcessor:
    """Task processor using regman."""

    def __init__(self) -> None:
        self.registry = Registry("task_processors")
        self._register_processors()
        self.results: List[Any] = []
        self.lock = threading.Lock()

    def _register_processors(self) -> None:
        """Registers all task processors."""

        @register(self.registry, "multiplier")
        class MultiplierProcessor:
            def process(self, data: int) -> int:
                time.sleep(0.1)  # Processing simulation
                return data * 2

        @register(self.registry, "squarer")
        class SquarerProcessor:
            def process(self, data: int) -> int:
                time.sleep(0.1)  # Processing simulation
                return data * data

        @register(self.registry, "incrementer")
        class IncrementerProcessor:
            def process(self, data: int) -> int:
                time.sleep(0.1)  # Processing simulation
                return data + 1

        @register(self.registry, "doubler")
        class DoublerProcessor:
            def process(self, data: int) -> int:
                time.sleep(0.1)  # Processing simulation
                return data * 2

    def process_task(self, processor_name: str, data: int) -> int:
        """Processes a task with a specific processor."""
        if processor_name not in self.registry:
            raise ValueError(f"Processor '{processor_name}' not available")

        processor_class = self.registry.get(processor_name)
        processor = processor_class()
        result = processor.process(data)

        # Thread-safe result addition
        with self.lock:
            self.results.append(
                {
                    "processor": processor_name,
                    "input": data,
                    "output": result,
                    "thread": threading.current_thread().name,
                }
            )

        return result

    def get_results(self) -> List[Any]:
        """Returns all results."""
        with self.lock:
            return self.results.copy()

    def clear_results(self) -> None:
        """Clears all results."""
        with self.lock:
            self.results.clear()

    def get_available_processors(self) -> List[str]:
        """Returns the list of available processors."""
        return self.registry.keys()


def worker_function(
    processor_name: str, data: int, task_processor: TaskProcessor
) -> int:
    """Worker function for a thread."""
    thread_id = threading.current_thread().name
    print(f"Thread {thread_id}: Processing {data} with {processor_name}")

    result = task_processor.process_task(processor_name, data)

    print(f"Thread {thread_id}: Result = {result}")
    return result


def main() -> None:
    """Concurrent usage example of regman."""
    print("=== Concurrent usage of regman ===\n")

    # Creating the task processor
    task_processor = TaskProcessor()

    # Displaying available processors
    print("1. Available task processors:")
    for processor_name in task_processor.get_available_processors():
        print(f"   - {processor_name}")
    print()

    # Sequential test
    print("2. Sequential test:")
    data = 5
    for processor_name in task_processor.get_available_processors():
        result = task_processor.process_task(processor_name, data)
        print(f"   {processor_name}({data}) = {result}")
    print()

    # Concurrent test
    print("3. Concurrent test:")
    task_processor.clear_results()

    # Data to process
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    processors = task_processor.get_available_processors()

    # Creating tasks
    tasks = []
    for i, data in enumerate(test_data):
        processor_name = processors[i % len(processors)]
        tasks.append((processor_name, data))

    print(f"   Processing {len(tasks)} tasks with {len(processors)} processors")
    print(f"   Using {min(4, len(tasks))} threads")
    print()

    # Concurrent execution
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(worker_function, processor_name, data, task_processor)
            for processor_name, data in tasks
        ]

        # Wait for all tasks to complete
        results = [future.result() for future in as_completed(futures)]

    end_time = time.time()
    duration = end_time - start_time

    print(f"\n   Execution time: {duration:.2f} seconds")
    print(f"   Tasks processed: {len(results)}")
    print()

    # Displaying results
    print("4. Detailed results:")
    all_results = task_processor.get_results()

    # Group by processor
    processor_results = {}
    for result in all_results:
        processor = result["processor"]
        if processor not in processor_results:
            processor_results[processor] = []
        processor_results[processor].append(result)

    for processor_name, results in processor_results.items():
        print(f"   {processor_name}:")
        for result in results:
            print(
                f"     Thread {result['thread']}: {result['input']} -> {result['output']}"
            )
    print()

    # Performance test
    print("5. Performance test:")

    # Sequential test
    task_processor.clear_results()
    start_time = time.time()

    for data in test_data:
        task_processor.process_task("multiplier", data)

    sequential_time = time.time() - start_time

    # Concurrent test
    task_processor.clear_results()
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(worker_function, "multiplier", data, task_processor)
            for data in test_data
        ]
        [future.result() for future in as_completed(futures)]

    concurrent_time = time.time() - start_time

    print(f"   Sequential time: {sequential_time:.2f} seconds")
    print(f"   Concurrent time: {concurrent_time:.2f} seconds")
    print(f"   Improvement: {sequential_time / concurrent_time:.2f}x")
    print()

    # Test with registry manager
    print("6. Test with registry manager:")

    manager = RegistryManager()

    # Creating multiple registries
    registry1 = manager.create_registry("workers")
    registry2 = manager.create_registry("managers")

    @register(registry1, "worker1")
    class Worker1:
        def work(self) -> str:
            return "Worker 1 is working"

    @register(registry1, "worker2")
    class Worker2:
        def work(self) -> str:
            return "Worker 2 is working"

    @register(registry2, "manager1")
    class Manager1:
        def manage(self) -> str:
            return "Manager 1 is managing"

    # Concurrent registry access test
    def access_registry(registry_name: str, worker_name: str) -> str:
        registry = manager.get_registry(registry_name)
        worker_class = registry.get(worker_name)
        worker = worker_class()
        return worker.work() if hasattr(worker, "work") else worker.manage()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(access_registry, "workers", "worker1"),
            executor.submit(access_registry, "workers", "worker2"),
            executor.submit(access_registry, "managers", "manager1"),
            executor.submit(access_registry, "workers", "worker1"),
        ]

        results = [future.result() for future in as_completed(futures)]

    print("   Concurrent registry access results:")
    for result in results:
        print(f"     {result}")

    print(f"\n   Total number of registries: {len(manager.all())}")
    print(f"   Available registries: {list(manager.all().keys())}")


if __name__ == "__main__":
    main()
