"""Furniture & prop kits (parametric, style-aware) and room decorators.

    from tools.voxel.kits import STYLES, furniture as F, rooms
    F.place(scene, F.bed(STYLES["noble"], double=True, canopy=True), at=(10, 1, 4), facing="south")
    rooms.furnish(scene, (x0, y0, z0, x1, y1, z1), "bedroom", "noble", doors=[(x, y, z)])
"""
from .style import STYLES, Style  # noqa: F401
from . import furniture  # noqa: F401
