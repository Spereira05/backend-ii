from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle:
    def draw(self):
        return "Drawing a circle"
        
class Square:
    def draw(self):
        return "Drawing a square"
        
def factory_of_shapes(shape_type):
    if shape_type == "circle":
        return Circle()
    elif shape_type == "square":
        return Square()
    else:
        return ValueError("unknown shape")
        
circle = factory_of_shapes("circle")
square = factory_of_shapes("square")

print(circle.draw())
print(square.draw())