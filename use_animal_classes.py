# Import the Animal and Dog classes from the tutorial file
from python_classes_tutorial import Animal, Dog

def main():
    # Create instances of Animal and Dog classes
    cat = Animal("Whiskers", "Cat")
    dog = Dog("Buddy", "Golden Retriever")

    # Access and modify attributes using properties
    print(f"Cat - Name: {cat.name}, Species: {cat.get_species()}")
    cat.name = "Mittens"
    cat.set_species("Feline")
    print(f"Updated Cat - Name: {cat.name}, Species: {cat.get_species()}")

    print(f"Dog - Name: {dog.name}, Species: {dog.get_species()}, Breed: {dog.get_breed()}")
    dog.name = "Max"
    dog.set_breed("Labrador")
    print(f"Updated Dog - Name: {dog.name}, Breed: {dog.get_breed()}")

    # Use static method
    print(f"Is Animal: {Animal.is_animal()}")

    # Use class method to create a new dog
    new_dog = Animal.create_dog("Rex")
    print(f"New Dog - Name: {new_dog.name}, Species: {new_dog.get_species()}")

    # Access class variable
    print(f"Kingdom: {Animal.kingdom}")

    # Use the public method that calls the private method
    human_years = 5
    print(f"Dog's age in animal years: {dog.get_age_in_animal_years(human_years)}")

if __name__ == "__main__":
    main()
