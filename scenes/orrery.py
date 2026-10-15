"""THE ORRERY OF AST: showcase build (concept B, evolved from scenes/concepts/arcane.py).

An astronomer-mage tore the summit off a mountain and hung it over the crater it left. On the floating summit stands a
ring-walled castle of needle towers around the Spire; three armillary rings turn around it on axles. Art direction:
scenes/orrery.md; pass notes: scenes/orrery.notes.md; room zones: docs/builds/orrery-zones.md.

Render: python -m tools.voxel render scenes/orrery.py --mood dusk
Parts: scenes/orrery_parts/ (terrain, island, castle, spire, rings, stair, rooms)."""
import importlib

from tools.voxel.scene import Scene

from scenes.orrery_parts import common as K

PARTS = ("terrain", "island", "castle", "spire", "rings", "stair", "moorings", "rooms", "finish")


def _mod(name):
    return importlib.import_module(f"scenes.orrery_parts.{name}")


def build():
    s = Scene((K.W, K.H, K.D), "orrery", seed=K.SEED)
    ctx = {}
    for p in PARTS:
        try:
            m = _mod(p)
        except ModuleNotFoundError as e:
            if e.name == f"scenes.orrery_parts.{p}":
                continue
            raise
        m.build(s, ctx)
    s.meta["report"] = {k: ctx[k] for k in ("ring_hits", "ring_hit_cells", "plugged", "fix_soil", "moorings") if k in ctx}
    s.meta["mood"] = "dusk"
    s.meta["origin"] = [-104, 20, -104]
    return s
