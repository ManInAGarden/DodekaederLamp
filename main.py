from build123d import *
from ocp_vscode import *
import math as m

from Dodecahedron import Dodecahedron
from SphericalProjector import SphericalProjector
from RegPentagon import RegPentagon
from AzimuthalEqudistantProjector import AzimuthalEquidistantProjector

# create a lamp which is like a ball of a given diameter with printable elements constructing a ball and connecting in the points goven
# by the corners of a dodecaeder which also are palced on the surface of the ball.

show_clear()

#parameters
diameter = 50*CM #the diameter of the ball
bandw = 10*MM
incdia = 2*bandw

#calculated - do not change
r = diameter/2  # diameter of the ball


a = Dodecahedron.get_a_from_outerrad(r)
dode_sk = Dodecahedron.getbasesketch(a)
dode_corners = Dodecahedron.get_corners_veclst(a)
penta_ukr = RegPentagon.get_outer_radius(a)
dc = dode_sk.center()
pc = Pos(dc)

startvec = Vector(penta_ukr,0)
startang =  -dode_corners[0].get_angle(Vector(penta_ukr,0))
skt = (
    Face()
    + PolarLocations(0,5,startang) * SlotCenterPoint((penta_ukr/2, 0), (0, 0), bandw)
    + Circle(2*bandw)
    - Circle(bandw)
)
#holes in the end of the fingers for connecting the parts
for corn in dode_corners:
    skt -= Location(corn)*Circle(3*MM)

skt.label = "CONSTR"

ri = Dodecahedron.rad_inner(a)
ro = Dodecahedron.rad_outer(a)
#a sperical projector for a sphere with radius r and centre in centre
spo = SphericalProjector(r, center=Vector(dc.X,dc.Y,ri))
sps = spo._mysphere

#now project the sketch
#ppsk = spo.project(skt)
ppsk = spo.project_face(skt)

azspro = AzimuthalEquidistantProjector(sphcenter=spo.center,
                                      sphrad=spo.radius)
azspro.set_proj_center(0, m.pi) #projection centre on the south pole

#planproj = azspro.project(ppsk)
#planproj.position -= (0, 0, ro + 10*MM)
projface = azspro.project(ppsk)
projface.position -= (0,0, ro + 10*MM)
#projface = make_face(planproj)
partex = extrude(projface, 1.2*MM)

dode = Pos(0,0, ri) * Dodecahedron(outerradius=r)
#show(skt, dode_sk, ppsk, planproj, partex)
show_all()
#show(Dodecahedron(outerradius=r))