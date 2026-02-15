from build123d import *
from ocp_vscode import *
from Dodecahedron import Dodecahedron
from RegPentagon import RegPentagon

import math as m

# parameters
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

# contructing Sketch for one of the fingers
spsk = Line((-deltm,-bandw/2),(-penta_ukr,-bandw/2))
spsk += ThreePointArc((-penta_ukr,-bandw/2),(-penta_ukr-bandw/2,0),(-penta_ukr,bandw/2))
spsk += Line((-penta_ukr,bandw/2), (-deltm,bandw/2))

#arranging/copying five fingers so that they touch the corners of a regular pentagon
psk = None
crnarcs = RegPentagon.get_corner_arcs()
for alph in crnarcs:
    if psk is None:
        psk = Rot(0,0,alph-180) * make_face(spsk)
    else:
        psk += Rot(0,0,alph-180) * make_face(spsk)

#adding the outer circle to connect the fingers
psk += pc * Circle(2*bandw)
#cutting out a while
psk -= pc * Circle(bandw)
psk.label = "CONSTR"

show_all()

for w in psk.wires():
    print(w.is_forward)
#all are foreward
#but look at the face - its correct

