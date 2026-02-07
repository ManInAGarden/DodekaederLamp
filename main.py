from build123d import *
from ocp_vscode import *
import math as m

from Dodecahedron import Dodecahedron
from SphericalProjector import SphericalProjector
from RegPentagon import RegPentagon
from AzimuthalEqudistantProjector import AzimuthalEquidistantProjecor

# create a lamp which is like a ball of a given diameter with printable elements constructing a ball and connecting in the points goven
# by the corners of a dodecaeder which also are palced on the surface of the ball.

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

deltm = m.sqrt(incdia**2 - bandw**2/4)
spsk = Line((-deltm,-bandw/2),(-penta_ukr,-bandw/2))
spsk += ThreePointArc((-penta_ukr,-bandw/2),(-penta_ukr-bandw/2,0),(-penta_ukr,bandw/2))
spsk += Line((-penta_ukr,bandw/2), (-deltm,bandw/2))

#psk = pc * Circle(2*bandw)
psk = None
crnarcs = RegPentagon.get_corner_arcs()
for alph in crnarcs:
    if psk is None:
        psk = Rot(0,0,alph-180) * make_face(spsk)
    else:
        psk += Rot(0,0,alph-180) * make_face(spsk)

psk += pc * Circle(2*bandw)
psk -= pc * Circle(bandw)

ri = Dodecahedron.rad_inner(a)
#a sperical projector for a sphere with radius r and centre in centre
spo = SphericalProjector(r, center=Vector(dc.X,dc.Y,ri))
sps = spo._mysphere

#now project the sketch
projs = []
for sh in psk.edges():
    projs.append(spo.project(sh))

projectpt = AzimuthalEquidistantProjecor.pt_onarc(0,m.pi, spo.radius)
azspro = AzimuthalEquidistantProjecor(sphcenter=spo.center,
                                      projcenterpt=projectpt, 
                                      sphrad=spo.radius,
                                      zeromed=Vector(1,0,0))

planproj =  []
for edg in projs:
    planed = azspro.project(edg)
    planproj.append(planed)

show_clear()
show(psk, dode_sk, projs, sps, planproj)
#show(Dodecahedron(outerradius=r))