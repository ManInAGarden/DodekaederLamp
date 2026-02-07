from build123d import *
from ocp_vscode import *
from SphericalProjector import SphericalProjector
from AzimuthalEqudistantProjector import AzimuthalEquidistantProjecor
import math as m


def rad(ang):
    return m.pi*ang/180

#parameter
sphdia = 100
sphrad = sphdia/2

#construct a point on the sphere with lat/long 
theta01_d = 20 #long
phi01_d = 45 #lat

theta02_d = 30 #long
phi02_d = -45 #lat


theta01 = rad(theta01_d)
phi01 = rad(phi01_d)

theta02 = rad(theta02_d)
phi02 = rad(phi02_d)

spro = SphericalProjector(sphrad)
sph = spro._mysphere

azp = AzimuthalEquidistantProjecor(sphrad=spro.radius)
pt1 = azp.pt_at(phi01, theta01)
pt2 = azp.pt_at(phi02, theta02)
ptm = azp.pt_at(phi01 + (phi02-phi01)/2, theta01 + (theta02-theta01))

sk = Sketch() + ThreePointArc(pt1, ptm, pt2)

pt1_p = azp.proj_point(pt1)
pt2_p = azp.proj_point(pt2)

skproj = azp.project(sk.edges())
show_all()