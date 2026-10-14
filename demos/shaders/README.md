# shaders (M1 spike, v2)
Custom per-player post effects from the game resource pack (`resourcepack/assets/nonios/post_effect`, GLSL in
`resourcepack/assets/nonios/shaders/post`). Menu: G -> "Demo: custom shaders".

## Layers
`/posteffect add` stacks effects on a player. The demo keeps one pick per **layer** (scores `demo.look`, `demo.col`,
`demo.line`, `demo.dist`) and rebuilds the stack in a fixed order on every change (`demo:fx/apply`):

| Layer      | Effects | Order |
|------------|---------|-------|
| Look       | reaper, cinematic, thermal, cosmic, monster (+ madness_1..3 on top at low HP), angel, neon | 1st |
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
- `cinematic` (the "RTX" feel): soft-knee bloom (4 blur passes), god rays from bright sky (radial march toward
  `RayOrigin` = above the screen top), depth haze, ACES tone map, warm/cool split toning, vignette, grain.
  It is screen-space only: rays come from bright sky *visible on screen*, there is no real light position.
  If rays look like they point the wrong way, flip `RayOrigin.y` (1.3 -> -0.3).
- `thermal`: angel infrared vision. Cold ironbow world, heat edges, glowing heat signatures that pulse faster when
  the target is weaker. Signature colour = HP bracket (see below).
- `cosmic` (v3, "magical light"): every light glows. Pass 1 finds lights by **local contrast** (pixel brighter than
  its ring of neighbours, as a ratio, so it fires at night and stays calm in daylight) + very bright pixels + a rim on
  sky pixels that touch geometry. These bloom at three scales with their own colours: a tight halo in the light's own
  colour, a violet/magenta aura, and a large teal/blue spill that also lights nearby terrain. The hue shifts drift
  slowly, the halos shimmer (animated noise), and small sharp lights sparkle with 4+4-point glints. At night the sky
  gets a deep-space grade and the large scale reads as nebula gloom; shadows get a cool lift so it stays playable.
  Best with many lights (torches, lanterns, lava, glowstone) and with the moon behind trees.
  Where the v2 "aura" came from: the old star pass treated any sky pixel brighter than its neighbours as a star. Next to
  a bright moon, every gap between dark leaves passed that test, and the blur passes spread that cluster into a coloured
  gloom around the tree. v3 does it on purpose and for every light, not only the sky.
- `monster` ("Hunger" vision, my pick for the monster class): blood-red monochrome, sight fades to murk past
  ~28 blocks (`Range`), near silhouettes get hot rims (prey stand out), barrel warp + colour split, and a
  double-thump heartbeat that pulses the vignette. Meant to feel predatory, not to give information.
  - **Heartbeat sound**: `nonios:monster.heartbeat` (`resourcepack/assets/nonios/sounds.json`, placeholder = vanilla warden
    heartbeat 1-4). The shader beats every 20 ticks (`fract(GameTime*1200)`, first thump at phase 0.10 = tick 2 of
    `gametime % 20`); `demo:monster/tick` reads `time query gametime` and plays the sound on tick 1 (one tick early for
    network latency). Both run on game time, so they stay locked, also with the day cycle frozen (game time always runs).
  - **Madness** (`madness.fsh`, Don't Starve-like insanity): HP% picks a tier, >60 none, <=60 `madness_1`, <=35 `madness_2`,
    <=15 `madness_3` (Intensity 0.35 / 0.65 / 1.0), stacked right on top of the look. Ink tendrils creep in from the screen
    edges and writhe inward (reach grows with the tier); shadow "watchers" with pale blinking eyes appear in the periphery
    (a new set every 6 s, more of them at higher tiers); reds drip down and colour channels smear apart; the view breathes
    and darkens on each heartbeat. Sounds: low-pitched soul-sand-valley whispers from behind you, left or right (about
    every 16 / 8 / 4 s per tier), plus a slowed cave drone at tier 3 (`monster.whisper`, `monster.drone`).
    Tier changes re-apply the stack (`demo:monster/changed`). Health is read every tick for players with the look.
- `angel` (#22): majestic, ethereal world: desaturated a little, shadows lifted to a soft violet-grey, highlights pushed to
  gold, gentle gold bloom (screen blend), bright depth haze (the sky is veiled too) and three layers of slowly rising,
  swaying, twinkling light motes. **Thermal only on living things**: the HP glow (same teams/colours as Thermal) gives
  the halo, white-hot outline and bracket pulse, and the entity **bodies** get the thermal ironbow palette tinted by
  their HP colour. Bodies are found with a marker: the demo overlay's `core/entity.fsh` sets the lowest bits of every
  opaque entity pixel to R odd / G even / B odd (invisible, +-1/255). The post shader votes over 3x3 pixels and
  only trusts the marker within ~30 px of a glowing outline, so blocks, item frames and the hand stay out (blocks hit
  the pattern 1 in 8 by chance; the outline gate removes those). Limits: the marker only exists with the demo overlay;
  very large/close mobs only heat up near their outline (the gate's reach); translucent entity parts (slime outer
  layer) are not marked. Thermal itself is unchanged.
- `neon` (#23, look): the whole image goes grey and dim (like Reaper), and the edges of every object glow as neon tubes
  in that object's **own** colour, fully saturated: depth creases/silhouettes (Laplacian of depth, zero on flat planes)
  plus colour edges (Sobel). Tube colour = the most colourful pixel next to the edge, pushed to full saturation (grey
  objects get pale white tubes). Three glow sizes (core, 3 px, 12 px x2) with a faint mains hum flicker.
- `rainbow`: hue cycling with an outward ripple (colour only, no distortion).
- `comic`: posterised colours, halftone dots in the shadows, paper highlights.
- `ink` / `fluorescent` (the old "Neon"): the same line shader (`ink.fsh`): dark comic lines, or glowing additive cyan lines.
- `planet`: a tiny spherical planet. A point at distance d drops by d^2 / 2R (R = `Radius`, 256 blocks), so terrain bends
  smoothly away over the horizon; no wobble, always on. It is a post effect (screen-space reprojection with the depth
  buffer, a fixed-point search of 6 steps): each pixel samples the image higher up by the drop of what is there. Core
  shaders would bend the real geometry, but their only per-player switch (night vision) is taken by Acid. Limits: it
  can only show what is on screen, so the sky fills the gap above the bent horizon (the top row is stretched where
  nothing exists); `TanHalfFov` (0.70 = FOV 70) should match your FOV setting; looking straight down shows little bend.
  Combines with Acid (Acid bends geometry, Planet then bends the image).
- `wobble`: wavy screen + pulsing chromatic split (screen-space; was "Acid" in v2, the colour cycling moved to `rainbow`).

## Acid (world warp)
The classic "acid" (GLSL shaders mod formula): with distance from you the world waves up and down and rotates around
you, so far terrain curls up over your head and covers the sky; the terrain near you stays still. It moves the vertices,
so it lives in **core shader overrides** (`demos/shaders/resourcepack/assets/minecraft/shaders/core`: terrain, block,
entity, particle `.vsh` + `lightmap.fsh`; `entity.fsh` only adds the Angel marker), shared code in `include/nonios_acid.glsl`). Resource-pack core overrides still
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

## Thermal / angel HP: how it works and its limits
A post shader only sees the final image: it cannot read entity health or the entity-outline buffer (`/posteffect`
chains only get `minecraft:main`). So the datapack encodes HP and the shader decodes it:
- While anyone has the Thermal or Angel look, every player and every `demo.patient` mob gets Glowing (hidden particles) and joins
  a team whose colour encodes its HP: red <= 30%, gold 31-65%, green >= 66%; light_purple > 40 HP (20 hearts),
  aqua > 80 HP (40 hearts), counting absorption (doubling tiers = log scale). `demo:hp/one`.
- The outline is drawn into the main image before post effects, so `thermal_sig` picks those colours out
  (brightness-normalised match) and `thermal` turns them into blurred heat halos with a white-hot core.

Limits: Glowing is visible to **everyone** (also without the shader: they see coloured outlines); the team colour
takes the scoreboard team slot (clashes with real team colours in the map, would need a per-team palette or
a resource-pack-only outline); any other red/gold/green/purple/aqua pixel with the outline's look can trigger a false
signature (rare in practice, tune `Tolerance`/`MinBright`); only 5 brackets; HP updates every tick but the
infinite Glowing has to be cleared when thermal is turned off (`demo:hp/off`, automatic when nobody uses it).
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
