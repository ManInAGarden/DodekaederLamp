from build123d import *
import math as m

from RegPentagon import RegPentagon
from BasePolyHedron import BasePolyHedron

class Dodecahedron(BasePolyHedron):

    @property
    def a(self):
        return self._a
        
    @property
    def botsk(self):
        return self._sk
    
    
    @classmethod
    def rad_outer(cls, a):
        return a/4 * (m.sqrt(5)+1) * m.sqrt(3)
    
    @classmethod
    def rad_inner(cls, a):
        return a/20 * m.sqrt(250 + 110* m.sqrt(5))
    
    @classmethod
    def to_rad(cl, ang: float):
        return 2*m.pi/360*ang
    
    @classmethod
    def get_a_from_outerrad(cl, r : float):
        return 4*r/((m.sqrt(5)+1)*m.sqrt(3))
    
    
    @classmethod
    def getbasesketch(cl, a:float):
        """
        Get a sketch for the basic pentagon forming the outer faces of the
        dodecahedron
        
        :param cl: Description
        :param a: length of the sides of the pentagon
        :type a: float
        """
        bvect = cl.get_corners(a)
        return Sketch() + Polyline(bvect, close=True)
    
    @classmethod
    def get_corners_veclst(cl, a) -> list[Vector]:
        penta = RegPentagon(a)
        
        return penta.corners
    
    @classmethod
    def get_corners(cl, a) -> tuple:
        """
        get the fivve corner of the vasic pentagon forming the outer faces of the dodecahedron
        in a way that the centre of the pentagon is in (0,0)

        :param cl: Description
        :param a: length of the sides of the basic pentagon
        :return: the positions of the corners
        :rtype: tuple
        """
        penta = RegPentagon(a)
        answ = []
        for corner in penta.corners:
            answ.append((corner.X, corner.Y))

        return tuple(penta.corners)


    def __init__(self, elen : float = None, 
                 outerradius : float = None):
        
        if elen is not None and outerradius is None:
            a = elen
        elif elen is None and outerradius is not None:
            a = self.get_a_from_outerrad(outerradius)
        else:
            raise Exception("Missing or too many parameters. Use outerradius or elen (edgelength), not noth, do define the dodecahedron")
        
        self._a = a
        alph = 108
        
        myfaces = []
        sk = self.getbasesketch(a) # the floor sketch
        self._sk = sk
        myfaces.append(make_face(sk))
        self._bot_center = sk.center()
        
        self._mycenter = self._bot_center + Vector(0,0,1*self.rad_inner(a))

        bet = 180 - 180*m.atan(2.0)/m.pi #angle between neighboruring faces


        h = RegPentagon.get_inner_radius(a)
        yh = -h -h*m.sin(self.to_rad(bet-90))
        zh = h*m.sin(self.to_rad(180-bet))
        sk2 = Rot(bet,0,0) * sk
        sk2 = Pos(0,yh,zh) * sk2
        myfaces.append(make_face(sk2))

        for i in range(1,5):
            angl = 72
            sk3 = Rot(0,0,angl) * sk2
            myfaces.append(make_face(sk3))
            sk2 = sk3

        cp = Plane(self.mycentre)

        mirrored = []
        for mf in myfaces:
            mmf = mirror(mf, cp)
            mmf = Pos(-self.mycentre.X, -self.mycentre.Y, 0) * mmf
            mmf = Rot(0,0,36)* mmf
            mmf = Pos(self.mycentre.X, self.mycentre.Y,0) * mmf
            mirrored.append(mmf)

        for mmf in mirrored:
            myfaces.append(mmf)

        #correct the centre of the dodecaeder faces
        for i in range(len(myfaces)):
            myfaces[i] = Pos(-self.mycentre.X, -self.mycentre.Y, -self.mycentre.Z) * myfaces[i]

        self._sk = Pos(0, 0, -self.mycentre.Z) * self._sk
        self._mycenter= self._mycenter - Vector(0, 0, self.mycentre.Z)
        self._bot_center = self._bot_center - Vector(0, 0, self.mycentre.Z)
        self._myfaces = myfaces

        sh = Shell(self._myfaces)
        sol = Solid(sh)

        super().__init__(sol)

    
                

