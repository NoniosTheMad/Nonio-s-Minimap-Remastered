# shaders (M1 spike)
Custom per-player post effects from the game resource pack (`resourcepack/assets/nonios/post_effect`).
G -> "Demo: custom shaders": Reaper, Acid, Reaper (no depth), Reaper + Acid, list, clear.

- `nonios:reaper` - black world, white outlines. Depth-buffer edges (`use_depth_buffer`) + faint luminance Sobel.
- `nonios:reaper_luma` - same look from colour only; diagnostic if depth sampling fails.
- `nonios:acid` - hue cycling, wavy UVs, chromatic aberration, animated via `Globals.GameTime` (0..1 per 20 min).

Tuning lives in the JSON `uniforms` blocks (no GLSL edit needed). If the reaper outlines look inverted/empty,
flip `DepthReversed` to 0.0.
