from build123d import *

class BasePolyHedron(BasePartObject):
    @property
    def mycentre(self):
        return self._mycenter
    
    
    @classmethod
    def rad_outer(cls, a):
        raise Exception("Override me")
    
    @classmethod
    def rad_inner(cls, a):
        raise Exception("Override me")


    def __init__(self, sol : Solid):
        super().__init__(sol)

    