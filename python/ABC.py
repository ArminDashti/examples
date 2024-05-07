# This code was generated by HuggingChat CohereForAI/c4ai-command-r-plus


from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

# Usage example
circle = Circle(5)
print("Circle area:", circle.area())

rectangle = Rectangle(4, 6)
print("Rectangle area:", rectangle.area())