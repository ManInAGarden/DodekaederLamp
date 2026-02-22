from OCP.BRep import BRep_Tool
from OCP.Geom import Geom_Plane
from OCP.gp import gp_Pln, gp_Ax3, gp_Pnt, gp_Dir
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.BRepLib import BRepLib
from build123d import *
from ocp_vscode import *

import math

def _wrap_pi(angle: float) -> float:
    """Wrap an angle to (-pi, pi]."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def _map_uv(
    uv: tuple[float, float], center: tuple[float, float]
) -> tuple[float, float]:
    """
    Map a spherical UV point to planar (x, y) using azimuthal equidistant mapping.

    Assumptions:
      - u is longitude (radians), periodic 2*pi
      - v is latitude  (radians), typically in [-pi/2, +pi/2]
      - Sphere radius R = 1 (scale later if needed)

    Args:
        uv: (u, v) = (lon, lat) in radians.
        center: (u0, v0) = (lon0, lat0) in radians for the projection center.

    Returns:
        (x, y) in the plane, where distance from origin equals great-circle arc length (R*theta).
    """
    lon, lat = uv
    lon0, lat0 = center

    dlon = _wrap_pi(lon - lon0)

    sin_lat0 = math.sin(lat0)
    cos_lat0 = math.cos(lat0)
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)

    # Central angle (theta) via spherical law of cosines
    cos_theta = sin_lat0 * sin_lat + cos_lat0 * cos_lat * math.cos(dlon)
    cos_theta = max(-1.0, min(1.0, cos_theta))  # numerical safety
    theta = math.acos(cos_theta)

    # Arc length on unit sphere
    rho = theta

    # Azimuth (bearing) from center to point
    y = math.sin(dlon) * cos_lat
    x = cos_lat0 * sin_lat - sin_lat0 * cos_lat * math.cos(dlon)
    azimuth = math.atan2(y, x)

    # Map to plane
    x_plane = rho * math.cos(azimuth)
    y_plane = rho * math.sin(azimuth)

    return x_plane, y_plane


def azimuthal_equidistant_projector_from_face(
    non_planar: Face, surface_point: tuple[float, float]
) -> Face:
    """
    Generate the azimuthal equidistant projection of a face projected to a sphere given a
    surface point in uv space (u is longitude (wraps 0 → 2π) and v is latitude (−π/2 → π/2).
    """
    if non_planar.geom_type != GeomType.SPHERE:
        raise ValueError("Only works with spheres")

    r = non_planar.radius

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

    uv_outer_wire = Wire(_get_uv_edges(non_planar.outer_wire()))
    uv_inners_wires = [Wire(_get_uv_edges(i)) for i in non_planar.inner_wires()]

    def _map_wire(w: Wire) -> list[Edge]:
        mapped_edges = []
        for e in w.edges():
            mapped_pnts = []
            e_positions = e.positions(linspace(0, 1, 20))
            for p in e_positions:
                p_mapped = _map_uv((p.X, p.Y), surface_point)
                mapped_pnts.append(p_mapped)
            mapped_edge = Spline(mapped_pnts)
            mapped_edges.append(mapped_edge)
        return mapped_edges

    mapped_outer = Wire(_map_wire(uv_outer_wire))
    mapped_inners = [Wire(_map_wire(i)) for i in uv_inners_wires]

    new_face = Face(mapped_outer, mapped_inners).scale(r)

    return new_face


target = Sphere(3)
skt = (Rectangle(3, 3) - Circle(1)).face()

skt.position += (0, 0, 12)
skt_projected = skt.project_to_shape(target, (0, 0, -1))[0]

a = azimuthal_equidistant_projector_from_face(skt_projected, (0, math.pi / 2))