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
    

    #def project(self, edgetoproject : Edge):
    def project(self, sk : Sketch) -> Sketch:
        answw = Sketch()
        edges = sk.edges()
        i = 0
        for e in edges:
            print(i, e.geom_type)
            pes = self.project_edge_to_shape(e,self._mysphere, center=self.center)

            answw += pes
            i += 1

        return answw

            

