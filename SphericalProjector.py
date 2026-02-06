from build123d import *

class SphericalProjector():

    @property
    def screen(self):
        return self._mysphere
    
    @property
    def radius(self):
        return self._r
    
    @property
    def center(self):
        return self._center
    
    def __init__(self, radius:float, center : Vector = Vector(0,0,0)):
        self._r = radius
        self._center = center
        self._mysphere = self.get_new_sphere()

    def get_new_sphere(self):
        return Pos(self._center) * Sphere(self._r)

    def project_pt(self, pt : Vector) -> Vector: 
        ptp = pt-self._center
        
        if ptp.length == 0:
            raise Exception("The center of the sphere cannot be projected because there's no direction of projection")
        
        f = self._r/ptp.length
        
        return (f * ptp) + self._center
    
    def project_circle(self, center : Vector, radius : float) -> Circle:
        ct = type(center)
        r1 = Vector(radius,0) + center
        r2 = Vector(-radius, 0) + center

        r1p = self.project_pt(r1)
        r2p = self.project_pt(r2)
        rad = r1p-r2p
        cp = r1p + 0.5*rad
        radp = 0.5*rad.length
        return Circle(radp).moved(Location(cp))

    
    def project(self, edgetoproject : Edge):
        wi = Wire([edgetoproject])
        projected_wires = wi.project_to_shape(self._mysphere, center=self._center)
        for w in projected_wires:
            projected_edges = w.edges()
        
        return projected_edges

            

