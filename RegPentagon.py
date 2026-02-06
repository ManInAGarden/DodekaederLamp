import math as m
from build123d import Vector

class RegPentagon():

    @classmethod
    def get_inner_radius(cls, a:float):
        return a/2.0 * m.sqrt(1+2/m.sqrt(5))
    
    @classmethod
    def get_outer_radius(cls, a:float) -> float:
        return a*m.sqrt((5 + m.sqrt(5))/10)
    
    @property
    def corners(self) -> list[Vector]:
        return self._edges
    
    @classmethod
    def get_corner_arcs(cls) -> list[float]:
        dalph = 72
        answ = [dalph/4]
        for i in range(1,5):
            answ.append(answ[-1] + dalph)
        
        return answ
    
    def __init__(self, a:float):
        """
        Create a pentagon with edges of length a and 
        it's centre in (0,0)
        
        :param self: Description
        :param a: The length of the edges of the regular pentagon
        :type a: float
        """
        self._a = a
        self._edges = self.get_edges()


    def get_edges(self) -> list[Vector]:
        """
        Get the edges of the pentagon
        
        :param self: Description
        """

        a = self._a
        topi = m.pi/180
        alphac = topi * 72.0
        ro = self.get_outer_radius(a) #diameter of the outer circle
        deltaalph = alphac
        startalph = -m.pi/2 - alphac/2
        answ = []
        ptnum = 0
        while ptnum < 5:
            alph = startalph + ptnum*deltaalph
            pt = Vector(ro*m.cos(alph), ro*m.sin(alph))
            ptnum += 1
            answ.append(pt)

        return answ
