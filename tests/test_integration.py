"""
Tests integration for the entire regman package.
"""

# mypy: ignore-errors

import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import pytest

from regman import Registry, RegistryManager, register


class TestIntegration:
    """Tests integration for the regman package."""

    def test_full_workflow_with_registry(self) -> None:
        """
        Scenario: Full workflow with a registry

        Expected:
        - Creation, addition, retrieval, deletion function
        - All operations are consistent
        - The registry maintains its state
        """
        # Create a registry
        registry = Registry("workflow_test")

        # Add elements
        registry.add("plugin1", "Plugin 1")
        registry.add("plugin2", "Plugin 2")
        registry.add("plugin3", "Plugin 3")

        # Verify the state
        assert len(registry) == 3
        assert "plugin1" in registry
        assert "plugin2" in registry
        assert "plugin3" in registry

        # Retrieve elements
        assert registry.get("plugin1") == "Plugin 1"
        assert registry.get("plugin2") == "Plugin 2"
        assert registry.get("plugin3") == "Plugin 3"

        # List all elements
        all_items = registry.list()
        assert len(all_items) == 3
        assert all_items["plugin1"] == "Plugin 1"
        assert all_items["plugin2"] == "Plugin 2"
        assert all_items["plugin3"] == "Plugin 3"

        # Delete an element
        registry.unregister("plugin2")
        assert len(registry) == 2
        assert "plugin2" not in registry

        # Verify that the other elements are still there
        assert "plugin1" in registry
        assert "plugin3" in registry

        # Clear the registry
        registry.clear()
        assert len(registry) == 0
        assert registry.keys() == []
        assert registry.list() == {}

    def test_full_workflow_with_decorator(self) -> None:
        """
        Scenario: Workflow complete with the decorator

        Expected:
        - The decorator works with different types of objects
        - The objects are registered correctly
        - The objects maintain their functionality
        """
        registry = Registry("decorator_workflow_test")

        # Register a class
        @register(registry, "test_class")
        class TestClass:
            def __init__(self, value: str) -> None:
                self.value = value

            def get_value(self) -> str:
                return self.value

        # Register a function
        @register(registry, "test_function")
        def test_function(x: int) -> int:
            return x * 2

        # Register a lambda
        @register(registry, "test_lambda")
        def test_lambda(x: int) -> int:
            return x + 1

        # Verify the registration
        assert len(registry) == 3
        assert "test_class" in registry
        assert "test_function" in registry
        assert "test_lambda" in registry

        # Retrieve and use the objects
        RetrievedTestClass = registry.get("test_class")
        retrieved_test_function = registry.get("test_function")
        retrieved_test_lambda = registry.get("test_lambda")

        # Test the class
        obj = RetrievedTestClass("test_value")
        assert obj.get_value() == "test_value"

        # Test the function
        assert retrieved_test_function(5) == 10

        # Test the lambda
        assert retrieved_test_lambda(5) == 6

    def test_full_workflow_with_manager(self) -> None:
        """
        Scenario: Workflow complete with the registry manager

        Expected:
        - Creation and management of multiple registries
        - Each registry is independent
        - All operations function
        """
        manager = RegistryManager()

        # Create multiple registries
        plugins_registry = manager.create_registry("plugins")
        handlers_registry = manager.create_registry("handlers")
        strategies_registry = manager.create_registry("strategies")

        # Add elements to each registry
        plugins_registry.add("plugin1", "Plugin 1")
        plugins_registry.add("plugin2", "Plugin 2")

        handlers_registry.add("handler1", "Handler 1")
        handlers_registry.add("handler2", "Handler 2")

        strategies_registry.add("strategy1", "Strategy 1")
        strategies_registry.add("strategy2", "Strategy 2")

        # Verify the state of each registry
        assert len(plugins_registry) == 2
        assert len(handlers_registry) == 2
        assert len(strategies_registry) == 2

        # Verify the independence of the registries
        assert "plugin1" in plugins_registry
        assert "plugin1" not in handlers_registry
        assert "plugin1" not in strategies_registry

        # Retrieve the registries via the manager
        retrieved_plugins = manager.get_registry("plugins")
        retrieved_handlers = manager.get_registry("handlers")
        retrieved_strategies = manager.get_registry("strategies")

        assert retrieved_plugins is plugins_registry
        assert retrieved_handlers is handlers_registry
        assert retrieved_strategies is strategies_registry

        # Verify that all registries are in the manager
        all_registries = manager.all()
        assert len(all_registries) == 3
        assert "plugins" in all_registries
        assert "handlers" in all_registries
        assert "strategies" in all_registries

    def test_complex_plugin_system(self) -> None:
        """
        Scenario: Complex plugin system

        Expected:
        - Creation of a complete plugin system
        - Management of different types of plugins
        - Usage of plugins via the registry
        """
        manager = RegistryManager()

        # Create registries for different types of plugins
        data_plugins = manager.create_registry("data_plugins")
        ui_plugins = manager.create_registry("ui_plugins")
        processing_plugins = manager.create_registry("processing_plugins")

        # Define base interfaces using ABC
        class DataPlugin(ABC):
            @abstractmethod
            def load_data(self, source: str) -> Any:
                pass

        class UIPlugin(ABC):
            @abstractmethod
            def render(self, data: Any) -> str:
                pass

        class ProcessingPlugin(ABC):
            @abstractmethod
            def process(self, data: Any) -> Any:
                pass

        # Register data plugins
        @register(data_plugins, "csv_loader")
        class CSVLoader(DataPlugin):
            def load_data(self, source: str) -> List[Dict[str, Any]]:
                return [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]

        @register(data_plugins, "json_loader")
        class JSONLoader(DataPlugin):
            def load_data(self, source: str) -> Dict[str, Any]:
                return {"id": 1, "name": "test"}

        # Register interface plugins
        @register(ui_plugins, "html_renderer")
        class HTMLRenderer(UIPlugin):
            def render(self, data: Any) -> str:
                return f"<div>{data}</div>"

        @register(ui_plugins, "json_renderer")
        class JSONRenderer(UIPlugin):
            def render(self, data: Any) -> str:
                return str(data)

        # Register processing plugins
        @register(processing_plugins, "data_cleaner")
        class DataCleaner(ProcessingPlugin):
            def process(self, data: Any) -> Any:
                if isinstance(data, list):
                    return [item for item in data if item.get("id") is not None]
                return data

        @register(processing_plugins, "data_validator")
        class DataValidator(ProcessingPlugin):
            def process(self, data: Any) -> Any:
                if isinstance(data, list):
                    return [item for item in data if "name" in item]
                return data

        # Use the plugin system
        CSVLoaderClass = data_plugins.get("csv_loader")
        HTMLRendererClass = ui_plugins.get("html_renderer")
        DataCleanerClass = processing_plugins.get("data_cleaner")

        # Create instances
        csv_loader = CSVLoaderClass()
        html_renderer = HTMLRendererClass()
        data_cleaner = DataCleanerClass()

        # Load data
        data = csv_loader.load_data(source="test.csv")
        assert len(data) == 2

        # Clean data
        cleaned_data = data_cleaner.process(data)
        assert len(cleaned_data) == 2

        # Render data
        rendered = html_renderer.render(cleaned_data)
        assert "<div>" in rendered

    def test_strategy_pattern_implementation(self) -> None:
        """
        Scenario: Implementation of the Strategy pattern

        Expected:
        - Creation of a strategy system
        - Switching between different strategies
        - Usage of strategies via the registry
        """
        registry = Registry("strategy_test")

        # Define the strategy interface using ABC
        class PaymentStrategy(ABC):
            @abstractmethod
            def pay(self, amount: float) -> str:
                pass

        # Implement different strategies
        @register(registry, "credit_card")
        class CreditCardStrategy(PaymentStrategy):
            def pay(self, amount: float) -> str:
                return f"Paid ${amount} with credit card"

        @register(registry, "paypal")
        class PayPalStrategy(PaymentStrategy):
            def pay(self, amount: float) -> str:
                return f"Paid ${amount} with PayPal"

        @register(registry, "bank_transfer")
        class BankTransferStrategy(PaymentStrategy):
            def pay(self, amount: float) -> str:
                return f"Paid ${amount} with bank transfer"

        # Context class that uses the strategies
        class PaymentProcessor:
            def __init__(self, strategy_name: str) -> None:
                strategy_class = registry.get(strategy_name)
                self.strategy = strategy_class()  # Create instance

            def process_payment(self, amount: float) -> str:
                return self.strategy.pay(amount)

        # Test different strategies
        credit_card_processor = PaymentProcessor("credit_card")
        paypal_processor = PaymentProcessor("paypal")
        bank_transfer_processor = PaymentProcessor("bank_transfer")

        assert (
            credit_card_processor.process_payment(100.0)
            == "Paid $100.0 with credit card"
        )
        assert paypal_processor.process_payment(50.0) == "Paid $50.0 with PayPal"
        assert (
            bank_transfer_processor.process_payment(200.0)
            == "Paid $200.0 with bank transfer"
        )

    def test_observer_pattern_implementation(self) -> None:
        """
        Scenario: Implementation of the Observer pattern

        Expected:
        - Creation of an observer system
        - Registration and notification of observers
        - Management of events via the registry
        """
        registry = Registry("observer_test")

        # Define the observer interface using ABC
        class Observer(ABC):
            @abstractmethod
            def update(self, event: str, data: Any) -> None:
                pass

        # Implement different observers
        @register(registry, "logger")
        class LoggerObserver(Observer):
            def __init__(self) -> None:
                self.logs = []

            def update(self, event: str, data: Any) -> None:
                self.logs.append(f"LOG: {event} - {data}")

        @register(registry, "email_notifier")
        class EmailNotifierObserver(Observer):
            def __init__(self) -> None:
                self.emails = []

            def update(self, event: str, data: Any) -> None:
                self.emails.append(f"EMAIL: {event} - {data}")

        @register(registry, "sms_notifier")
        class SMSNotifierObserver(Observer):
            def __init__(self) -> None:
                self.sms = []

            def update(self, event: str, data: Any) -> None:
                self.sms.append(f"SMS: {event} - {data}")

        # Class that notifies the observers
        class EventSubject:
            def __init__(self) -> None:
                self.observers = []

            def add_observer(self, observer_name: str) -> None:
                observer_class = registry.get(observer_name)
                observer = observer_class()  # Create instance
                self.observers.append(observer)

            def notify_observers(self, event: str, data: Any) -> None:
                for observer in self.observers:
                    observer.update(event, data)

        # Test the observer system
        subject = EventSubject()
        subject.add_observer("logger")
        subject.add_observer("email_notifier")
        subject.add_observer("sms_notifier")

        # Notify the observers
        subject.notify_observers(
            "user_login", {"user_id": 123, "timestamp": "2024-01-01"}
        )
        subject.notify_observers(
            "user_logout", {"user_id": 123, "timestamp": "2024-01-02"}
        )

        # Verify that all observers have been notified
        # Get the instances from the subject's observers list
        logger = subject.observers[0]  # First observer (logger)
        email_notifier = subject.observers[1]  # Second observer (email_notifier)
        sms_notifier = subject.observers[2]  # Third observer (sms_notifier)

        assert len(logger.logs) == 2
        assert len(email_notifier.emails) == 2
        assert len(sms_notifier.sms) == 2

        assert "user_login" in logger.logs[0]
        assert "user_logout" in logger.logs[1]

    def test_factory_pattern_implementation(self) -> None:
        """
        Scenario: Implementation of the Factory pattern

        Expected:
        - Creation of a factory system
        - Creation of objects via the registry
        - Management of different types of objects
        """
        registry = Registry("factory_test")

        # Define the base interface using ABC
        class Animal(ABC):
            @abstractmethod
            def make_sound(self) -> str:
                pass

        # Implement different animals
        @register(registry, "dog")
        class Dog(Animal):
            def make_sound(self) -> str:
                return "Woof!"

        @register(registry, "cat")
        class Cat(Animal):
            def make_sound(self) -> str:
                return "Meow!"

        @register(registry, "bird")
        class Bird(Animal):
            def make_sound(self) -> str:
                return "Tweet!"

        # Factory that uses the registry
        class AnimalFactory:
            @staticmethod
            def create_animal(animal_type: str) -> Animal:
                animal_class = registry.get(animal_type)
                return animal_class()

        # Test the factory
        dog = AnimalFactory.create_animal("dog")
        cat = AnimalFactory.create_animal("cat")
        bird = AnimalFactory.create_animal("bird")

        assert dog.make_sound() == "Woof!"
        assert cat.make_sound() == "Meow!"
        assert bird.make_sound() == "Tweet!"

    def test_concurrent_integration_workflow(self) -> None:
        """
        Scenario: Workflow integration with concurrency

        Expected:
        - All concurrent operations succeed
        - No data corruption
        - The system remains consistent
        """
        manager = RegistryManager()
        registry = manager.create_registry("concurrent_integration_test")

        def worker(thread_id: int) -> None:
            """Worker thread to test concurrency."""
            # Add elements
            for i in range(100):
                key = f"thread_{thread_id}_item_{i}"
                try:
                    registry.add(key, f"value_{thread_id}_{i}")
                except ValueError:
                    pass

            # Retrieve elements
            for i in range(100):
                key = f"thread_{thread_id}_item_{i}"
                try:
                    registry.get(key)
                except KeyError:
                    pass

            # List elements
            for _ in range(10):
                registry.keys()
                registry.list()

        # Launch multiple threads
        num_threads = 5
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Verify that the registry is in a consistent state
        assert isinstance(registry.keys(), list)
        assert isinstance(registry.list(), dict)
        assert len(registry.keys()) == len(registry.list())

    def test_error_handling_integration(self) -> None:
        """
        Scenario: Error handling in an integration workflow

        Expected:
        - Errors are handled correctly
        - The system continues to function
        - Errors do not affect other operations
        """
        manager = RegistryManager()
        registry = manager.create_registry("error_handling_test")

        # Add valid elements
        registry.add("valid_key", "valid_value")
        assert "valid_key" in registry

        # Try to add a duplicate key (must fail)
        with pytest.raises(ValueError):
            registry.add("valid_key", "another_value")

        # Verify that the original element is still there
        assert registry.get("valid_key") == "valid_value"

        # Try to retrieve a nonexistent key (must fail)
        with pytest.raises(KeyError):
            registry.get("nonexistent_key")

        # Verify that the valid operations still work
        registry.add("another_valid_key", "another_valid_value")
        assert len(registry) == 2

        # Test error handling with the manager
        manager.create_registry("valid_registry")
        assert "valid_registry" in manager.all()

        # Try to create a duplicate registry (must fail)
        with pytest.raises(ValueError):
            manager.create_registry("valid_registry")

        # Verify that the original registry is still there
        assert manager.get_registry("valid_registry") is not None

    def test_performance_integration(self) -> None:
        """
        Scenario: Test of integration performance

        Expected:
        - The operations are fast
        - The system can handle many elements
        - The performances remain acceptable
        """
        manager = RegistryManager()
        registry = manager.create_registry("performance_test")

        # Measure the time to add many elements
        start_time = time.time()
        num_elements = 10000

        for i in range(num_elements):
            registry.add(f"key_{i}", f"value_{i}")

        add_time = time.time() - start_time
        assert add_time < 1.0  # Must be fast

        # Measure the time to retrieve
        start_time = time.time()
        for i in range(0, num_elements, 100):  # Retrieve a sample
            registry.get(f"key_{i}")
        get_time = time.time() - start_time
        assert get_time < 0.1  # Must be very fast

        # Measure the time to list
        start_time = time.time()
        for _ in range(100):
            registry.keys()
            registry.list()
        list_time = time.time() - start_time
        assert list_time < 0.5  # Must be reasonable

        # Verify that all elements are there
        assert len(registry) == num_elements
        assert "key_0" in registry
        assert "key_9999" in registry
