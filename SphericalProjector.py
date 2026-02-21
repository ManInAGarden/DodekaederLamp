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
    

    def project_edge_to_shape(
        self,
        edg : Edge,
        target_object, #a Shape
        direction: VectorLike | None = None,
        center: VectorLike | None = None,
    ) -> list[Edge]:
        """Project Edge - COPY BECAUSE THE ORIGINAL CONTAINS AN ERROR

        Project an Edge onto a Shape generating new wires on the surfaces of the object
        one and only one of `direction` or `center` must be provided. Note that one or
        more wires may be generated depending on the topology of the target object and
        location/direction of projection.

        To avoid flipping the normal of a face built with the projected wire the orientation
        of the output wires are forced to be the same as self.

        Args:
          target_object: Object to project onto
          direction: Parallel projection direction. Defaults to None.
          center: Conical center of projection. Defaults to None.
          target_object: Shape:
          direction: VectorLike:  (Default value = None)
          center: VectorLike:  (Default value = None)

        Returns:
          : Projected Edge(s)

        Raises:
          ValueError: Only one of direction or center must be provided

        """
        wire = Wire([edg])
        projected_wires = wire.project_to_shape(target_object, direction, center)
        projected_edges = ShapeList()

        for w in projected_wires:
            for e in w.edges():
                projected_edges.append(e)

        return projected_edges
    

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

