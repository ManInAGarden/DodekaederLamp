from build123d import *
from ocp_vscode import *
from Dodecahedron import Dodecahedron
from RegPentagon import RegPentagon

#dode = Dodecahedron(50*CM)

penta = RegPentagon(50*CM)

sk = Sketch() + Polyline(penta.corners, close=True)
show(sk)