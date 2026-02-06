import math as m

class Vector2():

    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    
    def __mul__(self, other):
        ot = type(other)
        if ot is float or ot is int:
            return Vector2(self.x*other, self.y*other)
        else:
            raise Exception("Invalid operation for Vector multiplication")

    def __init__(self, x:float, y:float):
        self._x = x
        self._y = y

