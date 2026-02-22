from build123d import *
from BasePolyHedron import BasePolyHedron

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
    

    def project(self, sk: Sketch) -> Sketch:
        answ = Sketch()
        for w in sk.wires():
            print("CONSTR" + str(w.is_forward))
            pwires = w.project_to_shape(self._mysphere, center=self.center)
            for pw in pwires:
                answ += pw

        answ.label = "SP_" + sk.label #must be done here because answ is not really preserved during += operation
        return answ

    def project_face(self, fc : Face) -> Sketch:
        ow = fc.outer_wire()
        iws = fc.inner_wires()
        pow = ow.project_to_shape(self._mysphere, center=self.center)[0]

        answ = Sketch() + pow
        for iw in iws:
            #iwps.append(iw.project_to_shape(self._mysphere, center=self.center))
            answ += iw.project_to_shape(self._mysphere, center=self.center)
        
        answ.lab = "SP_" + fc.label #must be done here because answ is not really preserved during += operation

        return answ
    
    def project_multiple(self, fc : Face, bh: BasePolyHedron) -> Sketch:
        """project the given faces as if they were originally 
        placed on every face of the hedron.
        """
        fs = bh.faces()

        answ = Sketch()
        for f in fs:
            if not f.is_planar:
                raise Exception("project multiple works only with planar faces on the base hedron")
            #first move the original fact to the face of the polyhedron    
            #and align the centers
            fcp = f.center_location * fc
            answ += fcp

        return answ

