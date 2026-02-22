from build123d import *
from ocp_vscode import *
from AzimuthalEqudistantProjector import AzimuthalEquidistantProjector

skt = (Rectangle(3, 3) - Circle(1)).face()
skt.position += (0, 0, 12)
target = Sphere(10)
skt_projected = skt.project_to_shape(target, (0, 0, -1))[0]

azip = AzimuthalEquidistantProjector(sphrad=10)
azp = azip.set_proj_center(0,0) # proj-centre to the north pole

skt_azi_projected = azip.project(skt_projected)

show_all()
