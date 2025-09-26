# mypy: ignore-errors

"""
Factory pattern implementation example with regman.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from regman import Registry, register


class Animal(ABC):
    """Base interface for all animals."""

    @abstractmethod
    def make_sound(self) -> str:
        """Returns the animal's sound."""
        pass

    @abstractmethod
    def get_species(self) -> str:
        """Returns the animal's species."""
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Returns the animal's information."""
        pass


class Dog(Animal):
    """Dog."""

    def __init__(self, name: str = "Rex") -> None:
        self.name = name
        self.species = "Canis lupus"

    def make_sound(self) -> str:
        return "Woof! Woof!"

    def get_species(self) -> str:
        return self.species

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "species": self.species,
            "sound": self.make_sound(),
            "type": "Mammal",
        }


class Cat(Animal):
    """Cat."""

    def __init__(self, name: str = "Whiskers") -> None:
        self.name = name
        self.species = "Felis catus"

    def make_sound(self) -> str:
        return "Meow! Meow!"

    def get_species(self) -> str:
        return self.species

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "species": self.species,
            "sound": self.make_sound(),
            "type": "Mammal",
        }


class Bird(Animal):
    """Bird."""

    def __init__(self, name: str = "Tweety") -> None:
        self.name = name
        self.species = "Serinus canaria"

    def make_sound(self) -> str:
        return "Tweet! Tweet!"

    def get_species(self) -> str:
        return self.species

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "species": self.species,
            "sound": self.make_sound(),
            "type": "Bird",
        }


class Fish(Animal):
    """Fish."""

    def __init__(self, name: str = "Nemo") -> None:
        self.name = name
        self.species = "Amphiprion ocellatus"

    def make_sound(self) -> str:
        return "Blub! Blub!"  # Fish don't really make noise

    def get_species(self) -> str:
        return self.species

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "species": self.species,
            "sound": self.make_sound(),
            "type": "Fish",
        }


class AnimalFactory:
    """Factory for creating animals using regman."""

    def __init__(self) -> None:
        self.registry = Registry("animals")
        self._register_animals()

    def _register_animals(self) -> None:
        """Registers all animal types."""

        @register(self.registry, "dog")
        class DogClass(Dog):
            pass

        @register(self.registry, "cat")
        class CatClass(Cat):
            pass

        @register(self.registry, "bird")
        class BirdClass(Bird):
            pass

        @register(self.registry, "fish")
        class FishClass(Fish):
            pass

    def create_animal(self, animal_type: str, name: str = None) -> Animal:
        """Creates an animal of the specified type."""
        if animal_type not in self.registry:
            raise ValueError(f"Animal type '{animal_type}' not available")

        animal_class = self.registry.get(animal_type)

        if name:
            return animal_class(name)
        else:
            return animal_class()

    def get_available_types(self) -> List[str]:
        """Returns the list of available animal types."""
        return self.registry.keys()

    def get_animal_info(self, animal_type: str) -> Dict[str, Any]:
        """Returns information about an animal type."""
        if animal_type not in self.registry:
            raise ValueError(f"Animal type '{animal_type}' not available")

        # Create a temporary animal to get its information
        temp_animal = self.create_animal(animal_type)
        return temp_animal.get_info()


class Zoo:
    """Zoo that uses the animal factory."""

    def __init__(self) -> None:
        self.factory = AnimalFactory()
        self.animals: List[Animal] = []

    def add_animal(self, animal_type: str, name: str = None) -> Animal:
        """Adds an animal to the zoo."""
        animal = self.factory.create_animal(animal_type, name)
        self.animals.append(animal)
        print(f"Animal added: {animal.get_info()['name']} ({animal_type})")
        return animal

    def list_animals(self) -> None:
        """Lists all animals in the zoo."""
        print(f"\nZoo contains {len(self.animals)} animals:")
        for i, animal in enumerate(self.animals, 1):
            info = animal.get_info()
            print(f"  {i}. {info['name']} ({info['species']}) - {info['sound']}")

    def make_all_sounds(self) -> None:
        """Makes all animals make noise."""
        print("\nAll animals make noise:")
        for animal in self.animals:
            info = animal.get_info()
            print(f"  {info['name']}: {animal.make_sound()}")

    def get_animals_by_type(self, animal_type: str) -> List[Animal]:
        """Returns all animals of a given type."""
        return [
            animal
            for animal in self.animals
            if animal.__class__.__name__.lower() == animal_type.lower()
        ]


def main() -> None:
    """Factory pattern usage example."""
    print("=== Factory pattern with regman ===\n")

    # Creating the factory
    factory = AnimalFactory()

    # Displaying available animal types
    print("1. Available animal types:")
    for animal_type in factory.get_available_types():
        info = factory.get_animal_info(animal_type)
        print(f"   - {animal_type}: {info['species']} ({info['type']})")
    print()

    # Creating individual animals
    print("2. Creating individual animals:")

    dog = factory.create_animal("dog", "Buddy")
    cat = factory.create_animal("cat", "Fluffy")
    bird = factory.create_animal("bird", "Polly")
    fish = factory.create_animal("fish", "Goldie")

    print(f"   Dog: {dog.get_info()}")
    print(f"   Cat: {cat.get_info()}")
    print(f"   Bird: {bird.get_info()}")
    print(f"   Fish: {fish.get_info()}")
    print()

    # Testing sounds
    print("3. Animal sounds:")
    print(f"   {dog.get_info()['name']}: {dog.make_sound()}")
    print(f"   {cat.get_info()['name']}: {cat.make_sound()}")
    print(f"   {bird.get_info()['name']}: {bird.make_sound()}")
    print(f"   {fish.get_info()['name']}: {fish.make_sound()}")
    print()

    # Zoo simulation
    print("4. Zoo simulation:")
    zoo = Zoo()

    # Adding animals to the zoo
    zoo.add_animal("dog", "Rex")
    zoo.add_animal("cat", "Whiskers")
    zoo.add_animal("bird", "Tweety")
    zoo.add_animal("fish", "Nemo")
    zoo.add_animal("dog", "Max")
    zoo.add_animal("cat", "Luna")

    # List animals
    zoo.list_animals()

    # All animals make noise
    zoo.make_all_sounds()

    # Search animals by type
    print("\n5. Search animals by type:")
    dogs = zoo.get_animals_by_type("dog")
    cats = zoo.get_animals_by_type("cat")

    print(f"   Dogs in zoo: {len(dogs)}")
    for dog in dogs:
        print(f"     - {dog.get_info()['name']}")

    print(f"   Cats in zoo: {len(cats)}")
    for cat in cats:
        print(f"     - {cat.get_info()['name']}")

    # Error handling test
    print("\n6. Error handling test:")
    try:
        unknown_animal = factory.create_animal("dragon")
    except ValueError as e:
        print(f"   Expected error: {e}")

    # Dynamic animal creation
    print("\n7. Dynamic animal creation:")
    animal_types = ["dog", "cat", "bird", "fish"]
    names = ["Alpha", "Beta", "Gamma", "Delta"]

    for animal_type, name in zip(animal_types, names):
        animal = factory.create_animal(animal_type, name)
        print(f"   {name} ({animal_type}): {animal.make_sound()}")


if __name__ == "__main__":
    main()
