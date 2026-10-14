# shaders (M1 spike, v3)
Custom per-player post effects from the game resource pack (`resourcepack/assets/nonios/post_effect`, GLSL in
`resourcepack/assets/nonios/shaders/post`). Menu: G -> "Demo: custom shaders".

## Layers
`/posteffect add` stacks effects on a player. The demo keeps one pick per **layer** (scores `demo.look`, `demo.col`,
`demo.line`, `demo.dist`) and rebuilds the stack in a fixed order on every change (`demo:fx/apply`):

| Layer      | Effects | Order |
|------------|---------|-------|
| Look       | reaper, cinematic, thermal, cosmic, monster (+ madness_1..10 on top at low HP), angel, neon, alien | 1st |
| Colour     | rainbow, comic | 2nd |
| Lines      | ink, fluorescent | 3rd |
| Wobble     | wobble | 4th |
| Planet     | planet | last post effect (so the curvature carries everything else) |
| Acid       | world warp (core shaders, not a post effect) | bends the geometry itself, combines with all of the above |

Presets only set layers; an "x <category>" (REMOVE row) button while a preset is on removes the whole preset, and clicking an
active effect again turns it off. The current stack stays on the action bar. Presets only set layers (`demo:fx/preset`): **Cracy Frog** = wobble + rainbow (the old Acid), **Comic book** = comic + ink,
**Angel** = angel look, **Neon Reaper** = reaper + fluorescent, **Star trip** = cosmic + Acid, **Bad trip** = Acid + wobble + rainbow,
**Tiny planet** = cinematic + planet. Any combination works; some are
pointless (e.g. reaper + comic). Post effects are client state, so the stack is re-applied when a player rejoins.

## Effects
- `reaper`: black world, white outlines (depth edges + faint luma Sobel). Unchanged from v1. `reaper_luma` is removed.
- `cinematic` (v2, #62, rebuilt): a restrained film look. v1 was broken because it ran an ACES tone map on an image
  that is already display-ready (whites went grey, the frame murky), fanned fake god rays from a fixed point above the
  screen whatever the sun was doing, and washed distant terrain into grey haze with a seam at the sky. v2: highlight
  **halation** (bright pass blurred twice, red-orange, screen blend, plus a little neutral bloom), a gentle **S-curve**
  that keeps white white with slightly lifted blacks, a subtle **teal-shadow / warm-highlight** split tone, slightly
  less saturation in the shadows, a soft **vignette**, mid-tone weighted **grain** and **letterbox** bars for 2.39:1
  (at least 7 % per side on screens wider than that). `cine_bright`/`cine_rays` are still used by Angel.
- `thermal` (v3, #61): a FLIR-style infrared camera with the **ironbow** palette (black, indigo, purple, magenta, orange,
  yellow, white; reference: FLIR/ironbow descriptions and footage). Everything becomes one continuous temperature T,
  coloured through one smooth palette:
  - **sources only** are hot: living entities (orange-yellow), light-emitting blocks (lava, fire, torches, glowstone,
    lanterns...) and flames (white). Pass 1 (`thermal_heat.fsh`) finds them from the overlay markers (see "Markers");
    a block counts only on its own faces (block light >= 14) with a bright warm or white texture, and only if it is
    bright on screen, so lit floors, far terrain and stray bits stay cold (v2 painted the block-light bands and speckled).
  - **warmth around a source** = the source mask blurred at two sizes (6 px and 22 px, two box passes each), added
    with soft compression: smooth falloff, no bands.
  - **cold world**: scene brightness mapped into a narrow dark band, soft local detail, very faint depth edges, cooling
    with distance; sky coldest; the sun is hot, the moon not.
  - **hand / held item** (closer than 0.9 blocks) is neutral. Sensor noise and lens falloff are added before the palette.
  Limits: blended things (water, glass, clouds) read as cold; block entities (chests, signs, beds) are drawn as
  entities and read as warm; magma blocks and redstone torches emit too little light to count.
- `alien` (#54, the old Thermal, renamed): cold ironbow world, heat edges, glowing HP-coloured signatures that pulse
  faster when the target is weaker (HP tags, see below).
- `cosmic` (v4, #55): every light glows (v3: local-contrast light finder, three bloom scales with drifting hues,
  shimmer, glints on small lights), plus:
  - **the v2 halo is back on purpose**: `cosmic_aura.fsh` runs the old v2 star test (a sky pixel brighter than its
    neighbours). Next to a bright moon every gap between dark leaves passes it, and three blurs (4, 24, 24 px) spread the
    cluster into a violet/teal aura around the tree, which also spills a little onto the ground (`AuraSpill`).
  - **flower glitter** unchanged.
  - **sky**: the overlay's `core/sky.fsh` draws a nebula (two fbm colour fields along a galactic band) and stars into
    the sky disc, but only as a 2-bit code in the pixel's low bits (invisible without Cosmic). `cosmic.fsh` decodes it:
    violet/blue nebula clouds, stars with soft glow, 4-point spikes on the brightest, twinkle; the moon disc is boosted
    and gets a two-scale corona. Night only (fades in at dusk).
- `monster` ("Hunger" vision, my pick for the monster class): blood-red monochrome, sight fades to murk past
  ~28 blocks (`Range`), near silhouettes get hot rims (prey stand out), barrel warp + colour split, and a
  double-thump heartbeat that pulses the vignette. Meant to feel predatory, not to give information.
  - **Heartbeat sound**: `nonios:monster.heartbeat` (`resourcepack/assets/nonios/sounds.json`, placeholder = vanilla warden
    heartbeat 1-4). The shader beats every 20 ticks (`fract(GameTime*1200)`, first thump at phase 0.10 = tick 2 of
    `gametime % 20`); `demo:monster/tick` reads `time query gametime` and plays the sound on tick 1 (one tick early for
    network latency). Both run on game time, so they stay locked, also with the day cycle frozen (game time always runs).
  - **Taking damage** plays an extra hard heartbeat at once (`demo.dmg` = `damage_taken`, at most once per 10 ticks).
  - **Barrel warp drifts**: its centre and strength wander slowly (periods of ~25-50 s), so the lens never sits still.
  - **Madness** (`madness.fsh` v2, #58/#59): HP% sets a target level 0..10 (starts below 70 %, full at 15 %:
    `(75 - HP%) / 6`). The level **eases** toward it: one step every 4 ticks closing in, every 8 ticks letting go, so a
    burst of damage closes the tunnel over ~2 s and healing opens it slowly. Each level is its own JSON
    (`madness_1..10`, Intensity 0.1..1.0; a post shader keeps no state, so the datapack does the easing and a level change
    re-applies the stack, `demo:monster/changed`). Effects (no new ones, refined): the ink tunnel and up to 6 writhing
    tendrils reach in from the edges; the eyes are gone: **silhouettes** (tall thin figures with long arms, swaying,
    edges smoking away) stand at the edge of sight, and **faces** (pale, hollow eyes, a slowly opening mouth) surface
    only where the image is dark; a new set every 6 s, more at higher levels. Reds drip, the channel smear turns slowly,
    and the whole view drifts in a slow flow field (`Drift`) on top of the breathing swirl. Whispers every ~16 / 8 / 4 s
    at levels 2-4 / 5-7 / 8-10, cave drone at 8+.
- `angel` (v3, #57): majestic light. The white veil and the screen-space motes are gone. Now: a little exposure and
  saturation, a gold soft-knee bloom (less on the sky), **god rays** from bright sky (`cine_rays`, same as Cinematic),
  a warm distance **haze**, a light vignette and a soft highlight shoulder. **Motes** are real particles: `demo:angel/tick`
  (2 tries per tick per Angel player) picks a random column within 12 blocks, walks down to the first open block standing
  on something solid (`#demo:mote_air`), and spawns a rising `end_rod` mote and a little gold dust there; flowers also
  sparkle (`wax_off`). They are sent only to that player (`force @s`). HP behaviour unchanged: living things get the HP
  glow and the HP-tinted heat body (entity marker, see below), bodies never on the sky.
- `neon` (#23, look): the whole image goes grey and dim (like Reaper), and the edges of every object glow as neon tubes
  in that object's **own** colour, fully saturated: depth creases/silhouettes (Laplacian of depth, zero on flat planes)
  plus colour edges (Sobel). Tube colour = the most colourful pixel next to the edge, pushed to full saturation (grey
  objects get pale white tubes). Three glow sizes (core, 3 px, 12 px x2) with a faint mains hum flicker.
- `rainbow`: hue cycling with an outward ripple (colour only, no distortion).
- `comic`: posterised colours, halftone dots in the shadows, paper highlights.
- `ink` / `fluorescent` (the old "Neon"): the same line shader (`ink.fsh`): dark comic lines, or glowing additive cyan lines.
- `planet` (v2, #56): a tiny spherical planet. A point at distance d drops by d^2 / 2R (R = `Radius`, 256 blocks).
  Screen-space reprojection with the depth buffer: v1 iterated a fixed point per pixel, which jumped between solutions
  and tore clouds and edges. v2 marches each pixel's column upward (40 steps + 6 bisection steps) and takes the
  **first** crossing, so neighbouring pixels pick the same surface; gaps that open behind a bent edge are filled from
  the far side; the bend fades out toward the top of the screen (`FadeStart`), where the sky and clouds are, so they
  stay calm. Limits: it can only show what is on screen; `TanHalfFov` (0.70 = FOV 70) should match your FOV setting;
  looking straight down shows little bend. Combines with Acid (Acid bends geometry, Planet then bends the image).
- `wobble`: wavy screen + pulsing chromatic split (screen-space; was "Acid" in v2, the colour cycling moved to `rainbow`).

## Acid (world warp)
The classic "acid" (GLSL shaders mod formula): with distance from you the world waves up and down and rotates around
you, so far terrain curls up over your head and covers the sky; the terrain near you stays still. It moves the vertices,
so it lives in **core shader overrides** (`demos/shaders/resourcepack/assets/minecraft/shaders/core`: terrain, block,
entity, particle `.vsh` + `lightmap.fsh`; the `.fsh` files of terrain, entity, particle and sky only add markers, see below), shared code in `include/nonios_acid.glsl`). Resource-pack core overrides still
load in 26.3 (`ShaderManager` lists `shaders/` from all packs).

Per player switch: a core shader can't see scores or `/posteffect`, so the server drives a per-player value that reaches
the GPU: the **night vision** effect. The overridden `lightmap.fsh` no longer brightens with night vision and instead
writes the night vision factor into the lightmap alpha (1 - 8/255 when on); the vertex shaders read lightmap texel (0,0)
and warp when it is set. The button gives/clears `night_vision infinite` (hidden particles).

Limits / trade-offs:
- It is a demo overlay (only the shaders server's pack), because it changes vanilla shaders for everyone using the pack:
  real night vision (potions, conduit underwater) stops brightening and turns the warp on instead. Night vision still
  brightens the fog/sky colour (Java side), so the sky is a bit lighter while Acid is on.
- Chunk culling is done on the unwarped world: some bent terrain pops in or out at the screen edges; the sky and
  clouds are not bent (terrain covers them); held items/hand barely move (they are near the camera).
- With "Improved transparency" (OIT), the alpha-only pass of translucent blocks cannot read the lightmap, so water/glass
  may look slightly off while warped. Emissive entity layers (spider/enderman eyes) don't bend.
- The timing is the original's (cycles of ~45-80 s), mapped to `GameTime` so it loops seamlessly.
- **The sudden reset (#25)**: v1 of the port clamped two of the three time factors to a minimum size
  (`t = sign(t) * max(|t|, 0.35)`, meant to stop the warp from going flat). At every zero crossing that factor jumped from
  -0.35 to +0.35, so the curl flipped direction in one frame (about every 30-40 s). The clamp is gone; the factors are
  plain sines now, continuous at all times like the original (it briefly flattens at a crossing and comes back smoothly).
  GameTime wrap (integer cycles per day) and night vision (infinite, no flicker) were checked and are not causes.
- If core overrides break in a later version (26.4 moves to Vulkan), only this overlay breaks; the post effects are separate.

## Markers (overlay core shaders, invisible)
`include/nonios_mark.glsl`: every opaque pixel drawn by the overlay's `terrain`, `entity` and `particle` shaders gets its
lowest 2 bits per channel set (at most 3/255, invisible). Bit 0 is a tag (entity R1 G0 B1, terrain 0 1 0, particle 1 1 0),
bit 1 carries data: entity 000 (or 111 on emissive layers like spider eyes), terrain/particle a heat level 0..7
(non-zero only on light-emitting blocks and flames: block light >= 14 on the face x a bright warm/white texture). Sky pixels carry the Cosmic
nebula/star code instead. Post shaders decode with a 3x3 neighbour vote. Blended pixels (water, glass, clouds) are not
marked. The overlay is loaded for everyone on the demo server, but the marks change nothing visible.

## Alien / angel HP: how it works and its limits
A post shader only sees the final image: it cannot read entity health or the entity-outline buffer (`/posteffect`
chains only get `minecraft:main`). So the datapack encodes HP and the shader decodes it:
- While anyone has the Alien or Angel look, every player and every `demo.patient` mob gets Glowing (hidden particles) and joins
  a team whose colour encodes its HP: red <= 30%, gold 31-65%, green >= 66%; light_purple > 40 HP (20 hearts),
  aqua > 80 HP (40 hearts), counting absorption (doubling tiers = log scale). `demo:hp/one`.
- The outline is drawn into the main image before post effects, so `hp_sig` picks those colours out
  (brightness-normalised match) and `alien` turns them into blurred heat halos with a white-hot core.

Limits: Glowing is visible to **everyone** (also without the shader: they see coloured outlines); the team colour
takes the scoreboard team slot (clashes with real team colours in the map, would need a per-team palette or
a resource-pack-only outline); any other red/gold/green/purple/aqua pixel with the outline's look can trigger a false
signature (rare in practice, tune `Tolerance`/`MinBright`); only 5 brackets; HP updates every tick but the
infinite Glowing has to be cleared when nobody uses it (`demo:hp/off`, automatic when nobody uses it).
For the real game, prefer showing the HP through the outline colour only to the angel's team.

## World
The server runs on a pre-generated normal world, seed **2** (forest at spawn, river ~30 blocks, plains ~100, meadow hills ~100,
ocean ~270, snowy slopes ~1000). Scouted 32 seeds; none had real peaks inside view distance with spawn at sea level. mcdev can only create void/flat worlds, so the world was generated
on a scratch server and copied into `.mcdev/servers/shaders/world`. **G -> Reset this server turns it back into void**
(the gallery still builds, there is just no landscape).

## Materials gallery
`demo:build` (run once by `demo:ensure` on load, flag in storage `demo:state`; G -> Time & gallery -> Rebuild) carves a
plaza at spawn (x -21..21, z -9..43, floor y63) and builds: water and lava pools, glass / stained / tinted glass, ice,
light sources, wool / concrete / terracotta / stained-glass wall, ores, deepslate ores, metal blocks, stones, logs,
planks, grass / flowers / trees, a small house (furniture, lantern, bed), armour stands (leather to netherite, trims),
and NoAI "patients" for the HP test (villager low HP, sheep half, cow full, pig 50 HP, iron golem 100 HP).
Generated by a script; edit `build.mcfunction` directly for small changes.

## Time of day
Dawn 23400, Noon 6000, Dusk 12600, Midnight 18000 (`time set N`), cycle on/off = `gamerule advance_time`.

## Tuning
All knobs are JSON `uniforms` (no GLSL edit needed); the uniform list must keep the GLSL block's order and types.
If outlines/haze look inverted or empty, flip `DepthReversed` to 0.0. Bigger blur `Radius` = softer glow (costs GPU).
