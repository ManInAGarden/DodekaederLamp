from OCP.BRep import BRep_Tool
from OCP.Geom import Geom_Plane
from OCP.gp import gp_Pln, gp_Ax3, gp_Pnt, gp_Dir
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.BRepLib import BRepLib
from build123d import *
from ocp_vscode import show_all, show


def uv_wire_from_face(non_planar: Face) -> Face:
    """
    Convert the UV boundary of a non planar face into a planar 2D face.
    """
    _pln_xy = gp_Pln(gp_Ax3(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0.0, 0.0, 1.0)))
    _surf_xy = Geom_Plane(_pln_xy)

    def _get_uv_edges(w: Wire) -> list[Edge]:
        flat_edges = []
        for e in w.edges():
            curve = BRep_Tool.CurveOnSurface_s(
                e.wrapped, non_planar.wrapped, float(), float()
            )
            first, last = BRep_Tool.Range_s(e.wrapped, non_planar.wrapped)
            edge2d = BRepBuilderAPI_MakeEdge(curve, _surf_xy, first, last).Edge()
            BRepLib.BuildCurves3d_s(edge2d)
            flat_edges.append(Edge(edge2d))
        return flat_edges

    outer = Wire(_get_uv_edges(non_planar.outer_wire()))
    inner = [Wire(_get_uv_edges(i)) for i in non_planar.inner_wires()]

    new_face = Face(outer, inner)

    return new_face


target = Sphere(3)
skt = (Rectangle(3, 3) - Circle(1)).face()

skt.position += (0, 0, 12)
skt_projected = skt.project_to_shape(target, (0, 0, -1))[0]
flat = uv_wire_from_face(skt_projected)

skt2 = Plane.XZ * skt
skt2_projected = skt2.project_to_shape(target, (0, 1, 0))[0]

flat2 = uv_wire_from_face(skt2_projected)
show_all()