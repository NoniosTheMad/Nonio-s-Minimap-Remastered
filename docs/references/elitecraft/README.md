# EliteCraft 2 reference (ElRichMC)

Source: **ElRichMC — "EliteCraft 2 Ep 14, La base del administrador"**
https://www.youtube.com/watch?v=oj-qAh5RVW4 (all build credit goes to ElRichMC and the EliteCraft 2 builders).

Nonios picked this as the gold standard for detail, architecture and construction quality. The builder's breakdown is in [analysis.md](analysis.md).

## Images are local-only

This repo is public on GitHub, so the stills are **not committed**. They are copyrighted frames from someone else's video and are kept for private study only. `.gitignore` excludes `*.png`, `*.jpg` and `small/` in this folder. To regenerate them on another machine:

```
yt-dlp -f 303 -o video.webm https://www.youtube.com/watch?v=oj-qAh5RVW4      # 1080p60 VP9 (max available)
ffmpeg -ss 00:MM:SS -i video.webm -frames:v 1 frame_MMSS_topic.png           # per timestamp below
ffmpeg -i frame.png -vf scale=1600:-1 -q:v 3 small/frame.jpg
```

The best source available is 1920x1080 at 60 fps. The video has no 1440p or 4K stream.

## Frame index

Use the timestamps to scrub the video directly (`&t=MMmSSs`). Frames tagged *HUD* include the player's hand and hotbar.

| File | Time | Category | What it shows |
|---|---|---|---|
| frame_3940_establishing-bridge-dusk | 39:40 | Establishing | The best overall shot. A causeway leads to the keep, flanked by two round gate towers with flared red roofs and clustered grey pinnacles. Dusk sky, island of coarse dirt. |
| frame_3848_aerial-island-layout | 38:48 | Establishing | High aerial view of the whole compound: the island, the bridge axis and the keep plus its wings. |
| frame_1236_silhouette-dusk-keep | 12:36 | Silhouette | Night silhouette of the tall slab keep beside a smaller domed tower crowned with soul lanterns. |
| frame_3116_silhouette-from-sea | 31:16 | Silhouette | Distant view from the sea: the whole mass reads as one dark block with spiky skyline. *HUD* |
| frame_0156_main-facade-plaza | 01:56 | Facade | The central front: a giant wither-skull mosaic over the gate, a red/grey pointed portal, flanking towers with spike crowns, a red-roofed chapel wing on the right. |
| frame_0132_gatehouse-plaza-sunset | 01:32 | Facade / plaza | Side view of the gatehouse arch across the plaza, with soul-fire braziers and lamp posts. |
| frame_0136_facade-side-arch | 01:36 | Facade | Corner of the plaza: an arch opening, tower drums, lantern posts, water edge. |
| frame_2436_facade-pinnacles-plaza | 24:36 | Facade | Full front from mid-plaza, showing how the pinnacle rows build up in tiers toward the centre. *HUD* |
| frame_2424_plaza-braziers-wings | 24:24 | Plaza | Plaza with two big soul-fire braziers framing the facade. *HUD* |
| frame_0216_spire-shrine-tower | 02:16 | Spire / tower | A purple portal shrine with a stepped, spiky gable, plus a round tower with a pagoda-like flared red roof and attached pinnacle shafts. |
| frame_2420_spire-framed-buttress-towers | 24:20 | Spire / towers | The shrine on axis, framed by two leaning grey "fin" pinnacle clusters. *HUD* |
| frame_0220_entrance-recessed-arch | 02:20 | Entrance | **Best detail close-up.** About 6 nested recessed pointed arches in alternating grey and stone, red "flame" voussoirs radiating outward, stairs with a red runner, soul lanterns on the jambs. |
| frame_0420_hall-lava-runner-storage | 04:20 | Interior | The storage hall: walls of barrels and chests, a lava runner under red stained glass, a checker floor in grey/white/blackstone, and a pointed portal at the end. |
| frame_1352_hall-nave-perspective | 13:52 | Interior | The same hall shot down the nave: repeated red portal frames, shroomlight sconces, a rose-window mosaic at the end. *HUD* |
| frame_0508_ceiling-rose-window | 05:08 | Interior detail | The ceiling, looking straight up: a radial red/black rib vault around a blue glass rose. |
| frame_0608_corridor-red-runner | 06:08 | Interior | A narrow corridor with angled walls in red and blackstone bands and a red carpet runner. *HUD* |
| frame_0936_library-checker-floor | 09:36 | Interior | Library: a dark/birch-tone checker wood floor, bookshelf stacks, a lectern alcove. *HUD* |
| frame_2256_library-wide | 22:56 | Interior | The library seen wider, with a central lectern desk and red/black vaulting overhead. *HUD* |
| frame_2104_roof-terrace-brazier | 21:04 | Roof | A roof terrace with diagonal red stripes in the stair roofing and a soul-fire brazier. *HUD* |
| frame_1616_mining-hall-ore-wall | 16:16 | Interior | A utility/mining hall: long gallery with grey columns, an ore/diamond feature wall at the end. *HUD* |
| frame_0924_terrain-coarse-dirt-shore | 09:24 | Terrain | The base edge: coarse-dirt/rooted-dirt island blending into water, buildings meeting ground. *HUD* |
| frame_3528_map-plan-view | 35:28 | Plan | An in-game map art of the base, top-down: bastioned outline, round towers, radial plaza. |

## What the video is (and isn't)

This is a survival episode, not a cinematic showcase. About 60% of the runtime is inventories, books, chat, mining or a first-person HUD with the hand visible. The clean showcase moments are concentrated at 01:20–02:20, 04:20–05:20, 12:24–13:52, 24:20–24:40, 30:24–33:20 and 38:44–40:08.
