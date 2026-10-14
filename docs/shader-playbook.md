# Shader playbook (brief for future shader sessions)

Written after shader round 7 (#63-#66). Read this before you touch `resourcepack/assets/nonios/shaders/post`.

## 1. The loop that works: see it before the user does
Six rounds of "edit GLSL, sync, wait for in-game feedback" produced bugs that one look would have caught:
static below the horizon, a symbol on the moon, ghosts the user found laughable, and terrain moving in steps.
Claude can't watch the game, but it can look at images. So:

1. **Render offline first.** `tools/shaderlab/lab.py` runs the *real* post_effect JSON and `.fsh` files
   (uniform blocks rewritten, includes resolved, RGBA8 targets, `bilinear` honoured) on a ray-marched voxel
   scene with real-format reversed-Z depth and the overlay's low-bit markers (it includes the real `nonios_mark.glsl`).
   `python tools/shaderlab/lab.py --fx <effect> [--fx <next>] --time noon|dusk|night|<0..1> --shot walk|high|moon|treemoon|trees --frames 16 --out out/x --pngs`
2. **Read the contact sheet** (`out/x_sheet.png`) and single frames (`--pngs`). Critique in writing:
   what's wrong, where, and why (which term in which pass). Then change one thing.
3. **Reproduce the bug in the harness before fixing it.** For #64 the scene got an uncoded clear colour below the horizon.
   The old shader then showed the same white wall the user saw, and the fix could be checked against it.
4. **Test the edge cases on purpose**: night (most effects vanish on near-black), noon, looking at the
   sun or moon, high above the terrain (void below the horizon), and an ultra-wide screen (the user plays at 3440x1369).
5. **Show a reference animation** (`demos/shaders/reference/<fx>.gif`, at most about 1.5 MB) and only then sync to the server.
6. If `tools/mcfilm.py` is on `main`, film the real client to confirm. The harness has no entities, water, clouds or GUI.

## 2. Prompting / working habits that gave the best results
- **State the target look as references, not adjectives.** "Ethereal" alone produced a white veil. A good spec lists
  the components: volumetric shafts from the bright sky, a wide multi-scale bloom, a haze that brightens with distance,
  lifted pastel blacks, a few depth-faded bokeh motes. Name the Shadertoy/GPU Gems technique for each one.
- **Decompose into passes and own each term.** Write down which pass makes which visual. When something looks wrong,
  find the term that causes it, rather than retuning everything.
- **Diff against the version the user liked.** For "restore the old gloom", `git show <first commit>:<file>`. Port it
  term for term with the same constants, and say so in the header comment. Don't re-create it from memory: v4's
  "re-creation" kept one term out of four.
- **Never trust hidden data without a check.** Low-bit codes get scrambled by blending, the clear colour, and
  textures drawn on top. Put a check bit in the code (parity XOR a per-pixel key) and require the whole neighbourhood to pass.
- **Avoid per-pixel discontinuities in warps.** Any mapping driven by raw depth folds at every edge. Smooth the
  field that drives the warp, and search for the inverse on that smooth function.
- **No figurative horror from noise.** Procedural faces and figures read as cheesy. Abstract forms work better:
  ink, veins, thorns, pulsing seams.
- Use background forks for independent effects (one per effect, each with its own file scope, the parent commits).
  Give each a time box and an explicit "render, read, critique" loop count (at least 3 rounds).

## 3. Technique crib sheet (what the effects are built from)
| Look | Technique | Notes for MC post chains |
|---|---|---|
| Bloom | bright pass (soft knee) + blurs at 2-3 radii, summed (dual-filter / Kawase style) | `box_blur` needs `bilinear: true`. Without it, it skips every other pixel and aliases with dithered input |
| God rays | screen-space radial blur toward the light (GPU Gems 3, ch. 13: decay/weight/exposure) | find the light on screen from the brightest sky region. A fixed origin looks fake (Cinematic v1) |
| Haze / aerial perspective | `1 - exp(-density * dist)` toward a sky-tinted colour | linear distance from reversed-Z: `Near / d` |
| Motes / bokeh | hashed cells, soft discs, slow upward drift, depth-faded | few and soft. Real `end_rod` particles already exist for Angel |
| Creeping ink / madness | domain-warped fbm (Inigo Quilez, "warp"), threshold with a soft edge | an elliptical mask fitted to the screen aspect (0.7 between circle and screen) |
| Tendrils | polar coords + fbm, thickness tapers along the length, branching via a second noise | crawl inward with intensity. Animate on `GameTime` with whole cycles per day |
| Veins / cracks | Voronoi edge distance (F2 - F1) | pulse with the heartbeat phase |
| Star field / nebula | direction-keyed hash cells + fbm in the core sky shader, passed as a low-bit code | needs a check bit (see #64) |
| Planet curvature | shift = k * smoothed distance, inverse by column march + bisection + secant | smooth the distance (Gaussian, 16 bits in RG, `texelFetch`) |

## 4. Minecraft 26.3 post-chain gotchas
- Targets are RGBA8: no HDR between passes. Encode 16-bit values in two channels and never filter them.
- `use_depth_buffer` depth is reversed-Z here (`DepthReversed = 1`): sky = 0, linear distance = `Near / d`.
- A pass must not read and write the same target. Blur ping-pongs through `tmp`.
- Uniform lists in JSON must match the GLSL block order and types.
- Game-pack post shaders must not `#include` overlay-only files (the main server has no overlay).
- `GameTime` is 0..1 per 24000 ticks. Use whole multiples of TAU for seamless loops.
