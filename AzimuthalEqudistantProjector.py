from build123d import *
import math as m

class AzimuthalEquidistantProjecor():

    @classmethod
    def pt_onarc(cls, phi : float, theta : float, r : float, cent : Vector=Vector(0,0,0)):
        """
        get a point on the sphere given by the two angles and the radius of the sphere
        
        :param self: Description
        :param phi: Azimuthal angle (angle beween the projection of the point onto the xy-plane and the x-axis (1,0,0))
        :type phi: float
        :param theta: polar angle, angle between point an north pole vector (0,0,1*r)
        :type theta: float
        :param r : radius of the arc
        :type r : float
        :param cent: the centre of the sphere
        :type cent: Vector
        """
        x = r*m.sin(theta)*m.cos(phi)
        y = r*m.sin(theta)*m.sin(phi)
        z = r*m.cos(theta)

        return cent - Vector(x,y,z)


    def __init__(self, sphcenter:Vector=Vector(0,0,0), 
                 sphrad:float=1.0, 
                 projcenterpt:Vector=None,
                 zeromed:Vector=None):
        """
         erzeugt ein Exemplar der Klasse
        
        :param self: Description
        :param sphcenter: Vecor in R3 defining the centre where all other koordinates  ar erelated to
        :type sphcenter: Vector
        :param sphrad: radius of the sphere
        :type sphrad: float
        :param projcenterpt: The centre of the projection
        :type projcenterpt: Vector
        """
        self._sphcenter = sphcenter
        self._sphrad = sphrad

        if projcenterpt is None:
            scp = self.pt_at(0,0) #use the north pole
            self._zeromed = Vector(1,0,0)
        else:
            scp = projcenterpt
            if zeromed is None:
                raise Exception("you have to supply a zero meridian vector when you set a projection pt")
            
            self._zeromed = zeromed

        if not self._is_pt_on_sphere(scp):
            raise Exception("projection centre point mus be a point on the shpere that gets projected")
        
        self._projcenterpt = scp

    def set_proj_center(self, phi, theta):
        self._projcenterpt = self.pt_at(phi, theta)

    def to_rad(self, ang : float):
        return m.pi * ang/180
    
    def pt_at(self, phi : float, theta : float):
        """
        get a point on the sphere given by the two angles
        
        :param self: Description
        :param phi: Azimuthal angle (angle beween the projection of the point onto the xy-plane and the x-axis (1,0,0))
        :type phi: float
        :param theta: polar angle, angle between point an north pole vector (0,0,1*r)
        :type theta: float
        """
        r = self._sphrad
        x = r*m.sin(theta)*m.cos(phi)
        y = r*m.sin(theta)*m.sin(phi)
        z = r*m.cos(theta)

        return Vector(x,y,z)
    
    
    def _is_pt_on_sphere(self, ptt : Vector):
        return m.fabs(ptt.length - self._sphrad) < 1e-8
    
    
    def get_phitheta(self, pt : Vector):
        theta_d = self._projcenterpt.get_signed_angle(pt)
        theta = self.to_rad(theta_d)
        xypropt = Vector(pt.X, pt.Y)
        if xypropt.length < 1e-20:
            phi = 0
        else:
            phi_d = xypropt.get_signed_angle(self._zeromed)
            phi = self.to_rad(phi_d)
            
        return phi,theta
    

    def proj_outerpoint(self, pt : Vector) -> Vector:
        ptp = self.proj_point(self.to_relcoords(pt))
        return self.to_outercoords(ptp)
    
    def proj_point(self, pt : Vector) -> Vector:
        phi, theta = self.get_phitheta(pt)
        phic, thetac = self.get_phitheta(self._projcenterpt)

        rho = self._sphrad * m.fabs(theta - thetac)
        y = rho * m.sin(phi)
        x = rho * m.cos(phi)

        return Vector(x,y,0)
    
    def project_line(self, l : Line) -> Edge:
        st = l.start_point()
        end = l.end_point()
        stp = self.proj_outerpoint(st)
        endp = self.proj_outerpoint(end)
        answ = Edge.make_line(stp, endp)

        return answ

    def to_relcoords(self, v:Vector):
        return v - self._sphcenter
    
    def to_outercoords(self, v:Vector):
        return v + self._sphcenter
    
    def project_bspline(self, ed: Edge) -> Edge:
        ptps = []
        steps = 20
        stepsize = 1/20
        for i in range(0,steps+1):
            pf = i*stepsize
            pt = ed.position_at(pf)
            ptp = self.proj_outerpoint(pt)
            ptps.append(ptp)

        answ = Edge.make_spline(ptps)

        return answ

    def project_circle(self, ed: Edge) -> Edge:
        pc = ed.arc_center
        pc = self.to_relcoords(pc)

        if ed.is_closed: 
            # this only happends when the full circle is on the sphere
            # the procetion normally is a strangely bent curve
            pr = pc + Vector(ed.radius,0,0)

            pcp = self.to_outercoords(self.proj_point(pc))
            prp = self.proj_outerpoint(pr)
            outerkoordpl = Plane(pcp)
            rp = (prp - pcp).length
            answ = Edge.make_circle(rp, outerkoordpl)
            #answ = Pos(pcp) * Circle(rp)
            
        elif pc.length < 1e-15: #great circle
            #now the centre of that circle should be identical with the centre of the sphere 
            #and the projection is a straight line
            sp = ed.start_point()
            ep = ed.end_point()

            psp = self.proj_outerpoint(sp)
            pep = self.proj_outerpoint(ep)
            answ = Edge.make_line(psp, pep)
        else:
            #we haw an arc with a center somewhere on the sphere and start end endpt also on the sphere
            locs = ed.distribute_locations(10, positions_only=True)
            ptsp = []
            for loc in locs:
                v = Vector(loc.position.X, loc.position.Y, loc.position.Z)
                vp = self.proj_outerpoint(v)
                ptsp.append(vp)

            answ = Edge.make_spline(ptsp)            

        return answ

        
    def project(self, sk : Sketch) -> Sketch:
        answ = Sketch()
        wires = sk.wires()
        for w in wires:
            isi = w.is_interior
            edgesp = []
            for edg in w.edges():
                match edg.geom_type:
                    case GeomType.LINE:
                        newedge = self.project_line(edg)
                    case GeomType.CIRCLE:
                        newedge = self.project_circle(edg)
                    case GeomType.BSPLINE:
                        newedge = self.project_bspline(edg)
                    case _:
                        #print("not handled")
                        raise Exception("Unknown geometry type for projection")
                edgesp.append(newedge)

            wp = Wire(edges=edgesp, sequenced=True)
            answ += wp

        return answ
            



