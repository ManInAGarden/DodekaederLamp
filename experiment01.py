from build123d import *
from ocp_vscode import *

ball = Sphere(50*CM,arc_size1=45)
f = ball.faces().group_by(Axis.Z)[-1]

sk = Sketch() + Line((0,0),(60*CM,0))

show_all()
