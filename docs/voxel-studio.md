# Voxel studio

Builds (terrain, arenas, buildings) are written as **Python programs** that fill a numpy block grid. The studio renders
them headlessly so an agent can look at them, writes vanilla structure files, places them on an mcdev server over
RCON, reads the world back from the region files and diffs it against the source. In-game edits by the user become
a patch the agent can keep or fold into the code.

Design guidance (how to make a build look good, the critique prompt and the quality checklist) lives in
[`voxel-playbook.md`](voxel-playbook.md) (branch `feat/voxel-research`); research notes are in `voxel-research.md`.
This document covers the tool only.

Setup: `pip install -r tools/voxel/requirements.txt` (numpy, pillow, scipy, nbtlib, moderngl). Needs the 26.3 client
jar (CurseForge install path or `%APPDATA%\.minecraft`, or env `VOXEL_CLIENT_JAR`) and the server jar in `.tools/`.
On first use, the blockstates, models, textures and colormaps are extracted from the client jar to
`.mcdev/voxel/assets/26.3/`, and the block list (every block with its properties and defaults) comes from the
server's data report into `.mcdev/voxel/blocks-26.3.json`. All of this sits under the main checkout's `.mcdev/`,
which is gitignored. Mojang assets are never committed.

## The loop

```
author  scenes/x.py (build() -> Scene)                    one function per element, parameters at the top
render  python -m tools.voxel render scenes/x.py          iso x4, top, eye level per spawn/cam marker, sightlines, sheet.png
critique  read sheet.png (+ single views) with the playbook's critique prompt and checklist
revise  change one thing, state the expected visual change, re-render (about 3 s for 80x70x80)
place   python -m tools.voxel place scenes/x.py --server <name> [--pristine]
                                                          writes the tiles, places them, checks a sample with `execute if block`
user    walks it in game: chat lines / F2 screenshots / book = feedback (mcdev feedback); may edit blocks in creative
pull    python -m tools.voxel diff scenes/x.py --server <name>
                                                          save-all, read the box from the .mca files, diff it against the source,
                                                          then write the patch and render the diff views
merge   --patch keeps the edits as scenes/x.patch.json (applied after build()), or rewrite the code to match the edits and drop the patch
```

The agent opens images with its Read tool. `sheet.png` holds every view on one image, and the single PNGs give detail.
The outputs go to `.mcdev/voxel/out/<scene name>/`: `*.png`, `sheet.png`, `viewer.html`, `pulled.npz`, and
`diff/{sheet.png, patch.json}`.

## CLI (`python -m tools.voxel <cmd>`, run from the checkout root)

| command | what it does |
|---|---|
| `info SCENE` | Prints the size, bounds, palette counts, markers and meta. Lint flags gravity blocks over air, markers inside blocks and markers standing on air. |
| `render SCENE [--only iso,top,eye] [--size WxH] [--no-shadows] [--mood M]` | Writes the PNG views and the contact sheet. `--mood` sets sky, sun and block-light colour: `day` (default), `golden`, `dusk`, `night`, `ember`; a scene can set its own default with `meta["mood"]`. In non-day moods light sources (lava, lanterns, magma...) light their surroundings with a flood-filled block light and glow full-bright. |
| `view SCENE` | Writes `viewer.html`: a single offline file with three.js r147 inlined and real textures. Drag to orbit, right-drag to pan, wheel to zoom, keys 1-4 for the iso corners, T for top. |
| `export SCENE [--out DIR] [--tile 64] [--no-air]` | Writes structure `.nbt` tiles (DataVersion 5023, `{id, properties}` palette). |
| `place SCENE --server N [--at X Y Z] [--no-air] [--verify N] [--pristine]` | Places the scene at `--at`, else at the last placement, else at `meta["origin"]`. Air cells carve unless `--no-air`; `structure_void` cells leave the world alone. `--pristine` snapshots the world so mcdev's "Reset this server" restores the build. |
| `verify SCENE --server N [-n 300]` | Runs `execute if block` on random cells, half of them solid. Neighbour-shape properties are ignored. |
| `pull --server N (--box X0 Y0 Z0 X1 Y1 Z1 \| --scene SCENE) [--out F.npz]` | Reads a world box (inclusive) into a scene `.npz`. |
| `diff SCENE (--server N \| --against F.npz/.nbt) [--patch] [--strict] [--no-render]` | Prints the change summary: added/removed/replaced counts, the top transitions, and clusters in scene and world coordinates. Writes `patch.json` and renders the diff views: unchanged blocks dimmed, added green, replaced yellow, removed as red glass. |

SCENE can be a `.py` file (`build()` returning a Scene, or a module-level `SCENE`), a `.npz` written by `Scene.save`, or a structure `.nbt`.
For `.py` scenes the loader runs `build()`, then the auto-connect pass (`meta["connect"] = False` turns it off), then
`<scene>.patch.json` if one exists.

The server must be up (`mcdev up <name>`). The tool talks to it through the main checkout's `tools/mcdev.py`
(registry, RCON secret) and its world folder, `.mcdev/servers/<name>/world`. Templates are written to
`world/generated/voxel/structure/<scene>_<hash>_<ix>_<iz>.nbt`. The content hash in the name avoids the server's
template cache. Chunks in the box are force-loaded while placing. Every placement is logged to
`.mcdev/voxel/placements.json`, along with a snapshot `.npz` of exactly what was placed.

## Python API (`tools/voxel/`)

```python
from tools.voxel import shapes, noise
from tools.voxel.scene import Scene
from tools.voxel.palette import Mix, Gradient, Noise

s = Scene((80, 70, 80), "my_scene")               # idx[x, y, z] uint16, palette[0] = air
rock = (shapes.ellipsoid((40, 20, 40), (14, 12, 12)).smooth_union(shapes.sphere((30, 12, 46), 8), 3)
        .displace(amp=2.5, scale=6.5, seed=1))
s.fill(rock, Gradient("y", [(10, "cobbled_deepslate"), (20, Mix({"tuff": 3, "andesite": 1})), (99, "andesite")],
                      jitter=3, jitter_scale=7))   # clustered, value-ordered: dark low -> light high
s.decorate("grass_block", Mix({"short_grass": 5, "fern": 2}), chance=0.3)
s.mark("spawn_white", (12, 14, 40), look_at=(40, 25, 40))    # drives the eye-level renders and sightlines
s.meta["origin"] = [-40, 40, -40]                             # default placement
```

- **Block states** (`blockstate.py`): real 26.3 strings, for example `"stone_brick_stairs[facing=north,half=top]"`.
  The namespace is optional. Every state is validated against the block report. Typos raise an error with
  suggestions ("unknown block 'minecraft:chain' (did you mean minecraft:iron_chain ...)"). Missing properties are
  filled with their defaults. `rotate(state, k)` and `mirror_x` also turn facing, axis, rotation, stair shapes and
  connection properties.
- **Scene** (`scene.py`):
  - edits: `fill(where, spec, replace=)`, `box(p0, p1, spec, hollow=)` (inclusive corners like `/fill`), `set`, `line`, `replace`, `decorate(on, spec, chance)`
  - queries: `match(what)`, `solid()`, `surface()`, `counts()`, `bounds()`
  - modules: `stamp(module, at, rotate=, mirror=)`, `transformed`, `crop`
  - markers and io: `mark`, `save` / `load` (`.npz`)

  `where` can be an SDF, a bool grid or a pair of corners.
- **Shapes** (`shapes.py`): SDFs evaluated at voxel centres.
  - primitives: `sphere`, `ellipsoid`, `box`, `cylinder` (cone with `r_top`), `capsule`, `torus`, `half_space`, `heightfield`, `from_mask`
  - CSG: `|`, `&`, `-`, `smooth_union`, `smooth_subtract`
  - modifiers: `displace` (fbm), `shell`, `grow`, `translate`, `scale_y`, `twist`
- **Noise** (`noise.py`): vectorised improved Perlin `perlin`, `fbm`, `ridged`, and `hash` (deterministic per-voxel random).
- **Palettes** (`palette.py`): a spec is a state, `None` (keep), `Mix({state: weight})`,
  `Gradient(by, [(upto, spec), ...], jitter, jitter_scale)` or `Noise([(upto, spec)], scale)`. A callable can be a
  spec, and specs can nest.
  - `by`: `y`, `height` (0..1 within the fill), `depth` (solid blocks above), `exposure` (distance to air), `up` (top faces), `x`, `z`, or a callable.
  - Use `jitter_scale` > 0 for clustered (low-frequency) transitions. That is the playbook's "no stripes, no salt-and-pepper" rule.
- **Auto-connect** (`connect.py`): `connect(scene)` sets fence, pane, iron bars and wall connections (including tall/low
  sides and wall posts) and stair corner shapes, using the game's own rules. Verified: a placed scene pulled back
  matches with `--strict` (0 differences), so the renders show what the game shows. `sturdy(scene)` is the full-face
  mask (what vines, ladders and torches can attach to).
- **Rendering** (`mesh.py`, `render.py`): real block models (variants, multipart, element rotation, uvlock), cutout
  and translucent textures, biome tints (fixed plains), per-vertex AO, a 4096 sun shadow map, fog and 2x SSAA, on a
  moderngl standalone context.
  - Cameras: `iso_se/sw/nw/ne` (ortho, fitted to the geometry), `top` (north up), and `eye_<marker>` 1.62 above every `spawn_*/cam_*/eye_*` marker.
  - `sightlines.png` is a top map colouring each walkable cell by how many spawn/key markers can see it.
  - Speed: about 35k quads, 9 views in about 1.7 s (plus about 1.2 s to build the demo scene).
- **Structure IO** (`nbtio.py`): numpy-encoded writer (450k blocks in well under a second), `read_structure` for any
  version's `.nbt` (unknown states become `structure_void`).
- **Anvil reader** (`anvil.py`): `read_box(world, p0, p1)`. It reads the 26.3 layout `dimensions/minecraft/overworld/region`
  and handles both plain-string and `{id, properties}` palette entries. Unsaved chunks become `structure_void`
  (ignored by diff).
- **Diff** (`diff.py`): `diff(a, b, ignore_shape=True)`, then `.summary()`, `.patch()`, `.write_patch()` and
  `.render()`. `apply_patch(scene, path|list)` applies a patch.

## Demo: `ruined_tower` on server `voxel`

`scenes/ruined_tower.py` is a ruined watchtower on a moss-covered sky-island crag. It follows the playbook passes:
- brief, then a silhouette with three masses at different heights: tower, crag and curtain wall
- a value-ordered rock ramp (blackstone, cobbled_deepslate, deepslate/tuff, tuff/andesite, andesite/stone)
- masonry ramp: deepslate base, tuff bricks, stone bricks with mossy clusters, andesite top
- depth layers: battered plinth, stepped buttresses, string course and merlons, plus a stair path cut into the crag
- grounding: rubble heaps under the breach, fragments, moss sheets, vines on full faces only, azalea bushes

`demos/voxel` adds fixed afternoon light, no mobs, and a G dialog (2 columns, 7 fixed buttons plus mcdev's "What to
try here"): teleports to both spawns, the path and the tower interior, and creative/survival/spectator.

```
mcdev up voxel --branch feat/voxel-studio --demo voxel
python -m tools.voxel place scenes/ruined_tower.py --server voxel --verify 300 --pristine
python -m tools.voxel diff  scenes/ruined_tower.py --server voxel     # after the user's edits
```

## Known limits

- Block entities (chests, signs, banners, beds) and entities are not written to structures or read back: only block
  states are. In renders they appear as a simple cube with their particle texture.
- Water is rendered as a still 14/16-high block. Waterlogging, flowing water, biome-specific tints, emissive light
  and night lighting are not rendered.
- The game can change blocks after placement:
  - Unsupported blocks pop off (vines and torches without a full face, plants without soil); use `sturdy()`.
  - Gravity blocks over air fall (`info` lints these).
  - Leaves decay unless `persistent=true`.
  - Vines spread over time.

  `diff` shows all of these. Run it once right after placing to catch them.
- Placement replaces the whole box, air included. Use `--no-air` or `structure_void` cells to leave parts of the world alone.
- `pull` and `diff` need the box's chunks to have been saved at least once. Cells in never-generated chunks come back
  as `structure_void` and are not compared.
- The viewer bakes its lighting into the vertices: no shadows.
