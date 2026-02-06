from build123d import *
import math as m

class AzimuthalEquidistantProjecor():
    def __init__(self, sphcenter:Vector=Vector(0,0,0), 
                 sphrad:float=1.0, 
                 projcenterpt:Vector=None):
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
            scp = Pos(0,0,0)
        else:
            scp = projcenterpt

        if not self._is_pt_on_sphere(scp):
            self._chk = False
            scpint = self._correct_pt(scp)
            #when its not on the sphere correct it by elongating or shortening the vector
            sppt = scpint * (sphrad/scpint.length)
            scp = sppt
        else:
            scp = self._correct_pt(projcenterpt)

        self._chk = True
        self._projcenterpt = scp

    def to_rad(self, ang : float):
        return m.pi * ang/180
    
    def get_long_lat(self, x, y, z):
        phi = Vector(1,0,0).get_angle(Vector(x,y,0))
        lamb = Vector(1,0,0).get_angle(Vector(x,0,z))
        return self.to_rad(phi), self.to_rad(lamb)
    
    def _is_pt_on_sphere(self, ptt : Vector):
        return m.fabs(ptt.length - self._sphrad) < 1e-8
    
    def _correct_pt(self, pt : Vector) -> Vector:
        """
        transfer a point to the relative coordinate system of the projected
        spher
        
        :param self: Description
        :param pt: point to be transferred
        :type pt: Vector
        :return: transferred point
        :rtype: Vector
        """
        ptt = pt - self._sphcenter

        if self._chk :
            if not self._is_pt_on_sphere(ptt):
                raise Exception("A point that must be projected is not on the sphere")

        return ptt
    
    def _get_latlong(self, pt : Vector):
        zax = -1 * self._projcenterpt
        xax = -1 * Plane.XY.x_dir
        zax = Plane.XY.z_dir

        lambdadeg = xax.get_signed_angle(pt)
        phideg = zax.get_signed_angle(pt)

        return self.to_rad(phideg), self.to_rad(lambdadeg)


    def proj_point(self, pt : Vector) -> Vector:
        ptt = self._correct_pt(pt)
        phi, lam = self._get_latlong(ptt)
        phic, lamc = self._get_latlong(self._projcenterpt)
        sigma = m.atan((m.cos(phi)*m.sin(lam-lamc))/(m.cos(phic)*m.sin(phi)-m.sin(phic)*m.cos(phi)*m.cos(lam-lamc)))
        rho = self._sphrad * m.acos(m.sin(phic)*m.sin(phi) + m.cos(phic)*m.cos(phi)*m.cos(lam-lamc))
        
        x = rho * m.sin(sigma)
        y = rho * m.cos(sigma)

        return Vector(x,y,0)
    
    def proj_line(self, l : Line):
        st = l.start_point()
        end = l.end_point()
        stp = self.proj_point(st)
        endp = self.proj_point(end)

        return Line(stp,endp)

    def project_circle(self, ed: Edge):
        pc = ed.arc_center

        if ed.is_closed: 
            # this only happends when the full circle is on the sphere
            # the procetion normally is a strangely bent curve
            pr = pc + Vector(ed.radius,0,0)

            pcp = self.proj_point(pc)
            prp = self.proj_point(pr)

            rp = (prp - pcp).length
            answ = Pos(pcp) * Circle(rp)
        else:
            #now the centre of that circle should be identical with the centre of the sphere 
            #and the projection is a straight line
            sp = ed.start_point()
            ep = ed.end_point()

            psp = self.proj_point(sp)
            pep = self.proj_point(ep)
            answ = Line(psp, pep)
        return answ
    
    def project(self, eds : list[Edge]):

        answ = ShapeList()
        for edg in eds:
            match edg.geom_type:
                case GeomType.LINE:
                    newl = self.project_line(edg)
                    answ.append(newl)
                case GeomType.CIRCLE:
                    newcirc = self.project_circle(edg)
                    answ.append(newcirc)
                case _:
                    print(edg.geom_type)
                    #raise Exception("Unknown geometry type for projection")

        return answ
            



