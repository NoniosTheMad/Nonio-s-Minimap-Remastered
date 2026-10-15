# mcfilm: let agents see Minecraft

`tools/mcfilm.py` films a dev server with a second, real 26.3 client, so shader looks (post effects, core shaders,
resource pack) and voxel builds can be judged as rendered. It writes an **mp4** for the user plus **PNGs** for agents:
a contact sheet (3x3 grid of frames over time, each tile captioned with its timestamp) and the key frames at full size.
Agents can `Read` PNGs but not videos, so they review `sheet.png` and `frames/`.

## Quick use

```
# 6 s orbit around the shaders gallery at midnight with Thermal on
python tools/mcfilm.py shoot --server shaders --time midnight --setup "trigger demo.fx set 3" \
    --path tools/campaths/shaders_gallery.json --seconds 6 --out .mcdev/film/thermal

# a few fixed angles (one PNG each + sheet.png)
python tools/mcfilm.py still --server voxel --shot "-28 60 6 -90 10" --shot "8 70 40 180 15" --out .mcdev/film/tower

# several shots in a row: keep the session warm (~30 s boot saved per shot), close when done
python tools/mcfilm.py up --server shaders
python tools/mcfilm.py shoot --server shaders --keep ...
python tools/mcfilm.py cmd "posteffect clear {cam}"      # RCON on the cam server; {cam} = ClaudeCam
python tools/mcfilm.py close
```

Output (`--out`, default `.mcdev/film/<timestamp>`; a relative `--out` is relative to the main repo root, also from a
worktree): `video.mp4`, `sheet.png`, `frames/tNN.NNs.png`, `shot.json` (settings, frame count, `late_frames_repeated`,
`black_tiles`, and `client_warnings`: shader / post-effect / resource WARN and ERROR lines the cam client logged during
the shot, empty when everything loaded). `still`: `stillN.png` + `sheet.png`.

Check a shot by reading `sheet.png` (and a full frame from `frames/` for detail), then `shot.json`: `black_tiles` 0 and
`client_warnings` [] are the healthy values.

## Camera

- `--orbit "cx cy cz radius [height] [degrees] [start]"`: circle around a point, always looking at it.
  `start` = angle in degrees where 0 is south of the centre (+z) looking north; `degrees` defaults to 90.
- `--dolly "x1 y1 z1 x2 y2 z2 lx ly lz"`: straight move from 1 to 2 looking at l.
- `--at "x y z yaw pitch"`: fixed camera (good for animated effects: heartbeat, motes, wobble).
- `--path file.json`: keyframes or an orbit:
  ```json
  {"look_at": [0.5, 65, 10], "ease": true,
   "keys": [{"t": 0, "pos": [-10, 70, -5]}, {"t": 2, "pos": [0, 68, -8]}, {"t": 6, "pos": [12, 66, -4]}]}
  {"keys": [{"t": 0, "pos": [0, 70, 0], "yaw": 0, "pitch": 20}, {"t": 1, "pos": [0, 70, 10], "yaw": 90, "pitch": 10}]}
  {"orbit": {"center": [0.5, 64, 10], "radius": 14, "height": 6, "degrees": 120, "start": 0}}
  ```
  `t` is relative (scaled to `--seconds`). Without `look_at`, yaw/pitch are interpolated per key (shortest turn).
  `ease` (default true) smooths each segment. Examples in `tools/campaths/`.
- The camera is the player `ClaudeCam` in spectator mode, teleported every frame (`--fps`, default 20 = one move per
  server tick). Spectators fly through blocks, so paths can cross walls.

## Setup

- `--time dawn|noon|dusk|midnight|<ticks>`, `--weather clear|rain|thunder`.
- `--setup "<command>"` (repeatable, runs in order over RCON before filming). Commands starting with `trigger` run as
  the camera (`execute as ClaudeCam at @s run trigger ...`), with a tick between them (a trigger fires once per tick).
  `{cam}` is replaced by `ClaudeCam`. Anything else runs as the server (op level 4), e.g. `posteffect add {cam} nonios:reaper`.
- `--settle N` (default 3 s): wait after setup (chunks, effect warm-up, particles) before the first frame.
- `--hud`: keep the action bar and titles (blanked by default, see Limits).
- `--fov`, `--render-distance`.

Shaders demo triggers (`demo.fx`, from its dialogs): looks 1 Reaper, 2 Cinematic, 3 Thermal, 4 Cosmic, 5 Monster,
6 Angel, 7 Neon, 8 Alien; mix-ins 11 Rainbow, 12 Comic, 21 Ink, 22 Fluorescent, 31 Wobble; 35 Acid, 36 Planet;
presets 41 Cracy Frog, 42 Comic book, 43 Angel, 44 Neon Reaper, 45 Star trip, 46 Bad trip, 47 Tiny planet; 49 clear all;
time 60 Dawn, 61 Noon, 62 Dusk, 63 Midnight; 70 go to gallery. Clicking an active look again turns it off, so on a
kept session start with `trigger demo.fx set 49`.

Monster madness needs missing HP. Spectators take no damage, so lower health by raising max health instead
(regeneration off first, or it heals back):

```
# 20/52 HP = madness 6
python tools/mcfilm.py shoot --server shaders --time dusk --settle 4 --at "0.5 64 4.5 0 8" \
    --setup "trigger demo.fx set 49" --setup "gamerule natural_health_regeneration false" \
    --setup "attribute {cam} minecraft:max_health base set 20" \
    --setup "attribute {cam} minecraft:max_health base set 52" --setup "trigger demo.fx set 5"
```

Restore with `gamerule natural_health_regeneration true` and `max_health base set 20` before the next look.

Camera paths used for the samples (`tools/campaths/`): `shaders_gallery.json` (orbit over the gallery),
`shaders_dolly.json`, `cosmic_moon_trees.json` (midnight, moon through the treetops), `planet_walk.json` (walking
height down the pad), `angel_meadow.json` (glass/wool wall to the meadow), `voxel_tower.json` (whole ruined tower).

## How it works

1. **Cam server**: copies `.mcdev/servers/<server>/world` (datapack junctions are copied as files) to
   `.mcdev/cam/servers/<server>`, with the target's `server.properties` except: own ports (25700+, RCON +10000),
   `online-mode=false` (the camera is an offline account), `pause-when-empty-seconds=-1`, the resource pack served by
   mcfilm on port+100 with its sha1 and required. The pack is built from the target's sources (game pack + demo overlay,
   like mcdev). It is never in the mcdev registry: the daemon, idle sleep and G menus don't see it.
   The real server is only read: `list` (logged) and `save-all flush` over its RCON when it is up. Nothing else.
2. **Cam client**: vanilla 26.3 from the CurseForge install (`Install/versions/26.3`, libraries, assets, `java/java_25`),
   started by mcfilm with its own gameDir `.mcdev/cam/client`: offline user ClaudeCam (`--accessToken 0`), 1280x720
   window, sound off, chat hidden, pauseOnLostFocus off, inactivity FPS limit only when minimized, no onboarding/tutorial,
   and a `servers.dat` entry with server resource packs on (no prompt). `--quickPlayMultiplayer localhost:<port>` joins directly.
   After the join mcfilm hands focus back to the window that had it.
3. **Direction**: RCON on the cam server: spectator, the scoreboard displays cleared, setup, then one `tp` per frame.
4. **Capture**: `PrintWindow(PW_CLIENTONLY | PW_RENDERFULLCONTENT)` of the cam window: the window's own pixels even when
   other windows cover it. Raw frames are piped into ffmpeg (libx264, crf 20). If a frame is late the last one is repeated,
   so the video stays real time. ffmpeg: on PATH, else `.mcdev/tools/ffmpeg*/bin/ffmpeg.exe`, else it is fetched once
   from the `imageio-ffmpeg` wheel (pip download, ~30 MB, ffmpeg 7.1 with libx264) into `.mcdev/tools/ffmpeg-imageio/`.
5. **Cleanup**: `shoot`/`still` close the session at the end unless `--keep` or a session was already up. A detached
   watchdog (python, also the pack HTTP server) closes it when no mcfilm command touched it for `MCFILM_IDLE` seconds
   (default 600) or the mcfilm process that started it died. Kills are by PID only, after checking that the process command
   line points into `.mcdev\cam`. `close` also sweeps any java whose command line points there. The user's own client
   (CurseForge instance) is never touched. Log: `.mcdev/cam/mcfilm.log`.

## Limits

- **No F1.** 26.3's window is SDL3, which ignores key messages posted to an unfocused window, and stealing focus would
  disturb the user. Spectator mode already hides the hotbar, hand and the crosshair (it only shows over entities), chat is
  off, the sidebar/list/below-name displays are cleared on the copy, and the action bar and titles are blanked every
  frame. Bossbars and toasts can still show. The join toast ("chat messages can't be verified") is waited out.
- **The window must not be minimized** (a minimized window does not render). Covered is fine. It does appear on screen
  (and may take focus briefly when it opens); with the user at the PC, start it when they are not mid-fight.
- **Snapshot of the world**: the cam server is a copy taken at `up`. Builds made later on the real server need a new
  session (`close`, then shoot again). A changed resource pack restarts the session automatically.
- Motion is one teleport per tick (20 Hz): fast paths look steppy. Keep orbits slow (90-120 degrees in 6 s) or film at
  20 fps (default). Sound is not recorded.
- Per-player effects: anything the demo applies per player must be applied to `ClaudeCam` (triggers as above).
  HP-driven effects: see the Monster recipe above (no survival needed).
- `client_warnings` only catches what the client logs; a pass that compiles but draws wrong only shows in the frames.
- First run fetches ffmpeg (~30 MB). Boot: cam server ~10 s, client join ~25 s; later shots on a kept session ~10 s.
