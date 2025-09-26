# mypy: ignore-errors

"""
Plugin system example with regman.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from regman import Registry, register, RegistryManager


class Plugin(ABC):
    """Base interface for all plugins."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the plugin name."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Returns the plugin version."""
        pass

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Executes the plugin with the provided data."""
        pass


class DataProcessor(Plugin):
    """Data processing plugin."""

    def get_name(self) -> str:
        return "DataProcessor"

    def get_version(self) -> str:
        return "1.0.0"

    def execute(self, data: Any) -> Any:
        if isinstance(data, list):
            return [item * 2 for item in data]
        return data * 2


class TextFormatter(Plugin):
    """Text formatting plugin."""

    def get_name(self) -> str:
        return "TextFormatter"

    def get_version(self) -> str:
        return "1.2.0"

    def execute(self, data: Any) -> Any:
        if isinstance(data, str):
            return data.upper()
        return str(data).upper()


class DataValidator(Plugin):
    """Data validation plugin."""

    def get_name(self) -> str:
        return "DataValidator"

    def get_version(self) -> str:
        return "2.0.0"

    def execute(self, data: Any) -> Any:
        if isinstance(data, list):
            return [item for item in data if item is not None]
        return data if data is not None else None


class PluginManager:
    """Plugin manager using regman."""

    def __init__(self) -> None:
        self.manager = RegistryManager()
        self.plugins_registry = self.manager.create_registry("plugins")
        self._register_plugins()

    def _register_plugins(self) -> None:
        """Registers all plugins."""

        @register(self.plugins_registry, "data_processor")
        class DataProcessorPlugin(DataProcessor):
            pass

        @register(self.plugins_registry, "text_formatter")
        class TextFormatterPlugin(TextFormatter):
            pass

        @register(self.plugins_registry, "data_validator")
        class DataValidatorPlugin(DataValidator):
            pass

    def get_plugin(self, name: str) -> Plugin:
        """Retrieves a plugin by its name."""
        plugin_class = self.plugins_registry.get(name)
        return plugin_class()

    def list_plugins(self) -> List[str]:
        """Lists all available plugins."""
        return self.plugins_registry.keys()

    def execute_plugin(self, name: str, data: Any) -> Any:
        """Executes a plugin with data."""
        plugin = self.get_plugin(name)
        return plugin.execute(data)

    def get_plugin_info(self, name: str) -> Dict[str, str]:
        """Retrieves plugin information."""
        plugin = self.get_plugin(name)
        return {"name": plugin.get_name(), "version": plugin.get_version()}


def main() -> None:
    """Plugin system usage example."""
    print("=== Plugin system with regman ===\n")

    # Creating the plugin manager
    plugin_manager = PluginManager()

    # List of available plugins
    print("1. Available plugins:")
    for plugin_name in plugin_manager.list_plugins():
        info = plugin_manager.get_plugin_info(plugin_name)
        print(f"   - {plugin_name}: {info['name']} v{info['version']}")
    print()

    # Testing plugins
    print("2. Testing plugins:")

    # Test data processor
    data = [1, 2, 3, 4, 5]
    processed_data = plugin_manager.execute_plugin("data_processor", data)
    print(f"   Original data: {data}")
    print(f"   Processed data: {processed_data}")
    print()

    # Test text formatter
    text = "hello world"
    formatted_text = plugin_manager.execute_plugin("text_formatter", text)
    print(f"   Original text: {text}")
    print(f"   Formatted text: {formatted_text}")
    print()

    # Test data validator
    mixed_data = [1, None, 3, None, 5]
    validated_data = plugin_manager.execute_plugin("data_validator", mixed_data)
    print(f"   Mixed data: {mixed_data}")
    print(f"   Validated data: {validated_data}")
    print()

    # Processing pipeline
    print("3. Processing pipeline:")
    pipeline_data = [1, 2, None, 4, 5]
    print(f"   Initial data: {pipeline_data}")

    # Validation
    validated = plugin_manager.execute_plugin("data_validator", pipeline_data)
    print(f"   After validation: {validated}")

    # Processing
    processed = plugin_manager.execute_plugin("data_processor", validated)
    print(f"   After processing: {processed}")

    # Formatting
    formatted = plugin_manager.execute_plugin("text_formatter", processed)
    print(f"   After formatting: {formatted}")


if __name__ == "__main__":
    main()
