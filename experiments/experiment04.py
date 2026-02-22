from build123d import *
from ocp_vscode import *
import math as m

#parameters
diameter = 50*CM #the diameter of the ball
bandw = 10*MM
incdia = 2*bandw

r = diameter/2 ## radius of outer sphere of dodecahedron
a = 4*r/((m.sqrt(5)+1)*m.sqrt(3)) #lenght of the dodecahedron's edges
ri = a/20 * m.sqrt(250 + 110* m.sqrt(5)) # radius of inner sphere of dodecahedron
penta_ukr = a*m.sqrt((5 + m.sqrt(5))/10) # radius of circle touching all the corners of a pentagon face of the dodecahedron
deltm = m.sqrt(incdia**2 - bandw**2/4)
spsk = Line((-deltm,-bandw/2),(-penta_ukr,-bandw/2))
spsk += ThreePointArc((-penta_ukr,-bandw/2),(-penta_ukr-bandw/2,0),(-penta_ukr,bandw/2))
spsk += Line((-penta_ukr,bandw/2), (-deltm,bandw/2))

psk = None
for alph in [18,90,162,234,306]:
    if psk is None:
        psk = Rot(0,0,alph-180) * make_face(spsk)
    else:
        psk += Rot(0,0,alph-180) * make_face(spsk)

psk += Circle(2*bandw)
psk -= Circle(bandw)

cent = Vector(0,0,ri)
sph = Pos(cent) * Sphere(r)

projs = []
edc = len(psk.edges())
print(edc)
for ed in psk.edges():
    wi = Wire([ed])
    projected_wires = wi.project_to_shape(sph, center=cent)
    for w in projected_wires:
        projected_edges = w.edges()

    if(len(projected_wires)<1):
        raise Exception("Mist1")
        
    projs.append(projected_edges)
    #the follwing does not work
    #proj = ed.project_to_shape(sph, center=cent)
    #projs.append(proj)

show(psk.edges(), projs, sph)