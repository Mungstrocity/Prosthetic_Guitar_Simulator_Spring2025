# This is a basic tutorial on how to use classes in Python.

# Define a simple class
class Animal:
    # Class variable
    # Class variables are shared among all instances of the class.
    kingdom = "Animalia"

    # Constructor method
    # The constructor (__init__) is called when an instance (object) of the class is created.
    # It initializes the object's attributes.
    def __init__(self, name, species):
        self._name = name
        self.species = species

    # Destructor method
    # The destructor (__del__) is called when an instance (object) of the class is about to be destroyed.
    # It is used to perform any cleanup activities.
    def __del__(self):
        print(f"Animal object with name {self._name} and species {self.species} is being destroyed")

    # Property for name
    # Properties allow for controlled access to instance attributes.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Method to get the species of the animal
    def get_species(self):
        return self.species

    # Method to set the species of the animal
    def set_species(self, species):
        self.species = species

    # Private method example
    # Private methods are intended to be used only within the class.
    # They are typically used for internal helper functions.
    # Private methods are designated by prefixing the method name with double underscores (__).
    def __calculate_age_in_animal_years(self, human_years):
        # Example conversion: 1 human year = 7 animal years
        return human_years * 7

    # Public method that uses the private method
    def get_age_in_animal_years(self, human_years):
        return self.__calculate_age_in_animal_years(human_years)

    # Static method example
    # Static methods do not require access to the instance or class and are defined using the @staticmethod decorator.
    # Use static methods when you need a utility function that doesn't depend on instance or class state.
    @staticmethod
    def is_animal():
        # Practical example: Check if a given species is part of the animal kingdom
        return True

    # Class method example
    # Class methods have access to the class itself and are defined using the @classmethod decorator.
    # Use class methods for factory methods that need to create instances of the class.
    # The `cls` parameter represents the class itself, and is used to create new instances of the class.
    @classmethod
    def create_dog(cls, name):
        # Practical example: Create a new instance of Animal with species set to "Dog"
        return cls(name, "Dog")

# Create an instance of the Animal class
# The constructor is called here to create a new Animal object.
dog = Animal("Buddy", "Dog")

# Accessing attributes and methods using properties
print(f"Name: {dog.name}, Species: {dog.get_species()}")

# Modifying attributes using properties
dog.name = "Max"
dog.set_species("Canine")

print(f"Updated Name: {dog.name}, Updated Species: {dog.get_species()}")

# Using static method
print(f"Is Animal: {Animal.is_animal()}")

# Using class method
new_dog = Animal.create_dog("Rex")
print(f"New Dog - Name: {new_dog.name}, Species: {new_dog.get_species()}")

# Accessing class variable
print(f"Kingdom: {Animal.kingdom}")

# Using the public method that calls the private method
human_years = 5
print(f"Age in animal years: {dog.get_age_in_animal_years(human_years)}")

# Inheritance example
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    # Method to get the breed of the dog
    def get_breed(self):
        return self.breed

    # Method to set the breed of the dog
    def set_breed(self, breed):
        self.breed = breed

    # Overriding a method
    # Method overriding allows a subclass to provide a specific implementation of a method that is already defined in its superclass.
    def get_species(self):
        return f"{self.species} (overridden)"

# Create an instance of the Dog class
# The constructor is called here to create a new Dog object.
golden_retriever = Dog("Charlie", "Golden Retriever")

print(f"Name: {golden_retriever.name}, Species: {golden_retriever.get_species()}, Breed: {golden_retriever.get_breed()}")

# Modifying attributes using methods
golden_retriever.name = "Buddy"
golden_retriever.set_breed("Labrador")

print(f"Updated Name: {golden_retriever.name}, Updated Breed: {golden_retriever.get_breed()}")

# Explanation:
# The private method __calculate_age_in_animal_years is used to convert human years to animal years.
# Making this method private ensures that it is only used within the class and not accessible from outside.
# This encapsulation helps to hide the internal implementation details and provides a cleaner public interface.

# The static method is_animal is a utility function that checks if a given species is part of the animal kingdom.
# Static methods are useful for functions that don't need access to instance or class state.

# The class method create_dog is a factory method that creates a new instance of Animal with the species set to "Dog".
# Class methods are useful for creating alternative constructors or factory methods.
