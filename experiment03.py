from build123d import *
from ocp_vscode import *

from Dodecahedron import Dodecahedron

#dode = Dodecahedron(20*CM)

bsk = Dodecahedron.getbasesketch(20*CM)
dode = Dodecahedron(20*CM)
sk = Sketch() + Line((-60.0*CM,0),(60*CM,0)) + Line((0,-60*CM),(0,60*CM)) + Plane.XZ * Line((0,-60*CM),(0,60*CM))


show_all()