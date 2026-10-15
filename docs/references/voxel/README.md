# Voxel moodboard (calibration references)

These references calibrate **craft**: scale, composition, depth, density, cohesion and interiors. They are **not
themes to copy** (see [`../../voxel-playbook.md`](../../voxel-playbook.md) §1). How they are used is described in
[`../../voxel-research-2.md`](../../voxel-research-2.md). High-resolution EliteCraft frames and the builder's
breakdown live in [`../elitecraft/`](../elitecraft/).

## Images are local-only

All images belong to their creators. This repo is public, so the image files are **not committed**: `.gitignore`
excludes `*.jpg` and `*.png` in this folder. Use them only for private study and critic calibration. To fetch them on
another machine, run the commands below from this folder.

| File | What it shows | Credit / source |
|---|---|---|
| `elrichmc_elitecraft2_ep14_maxresdefault.jpg`, `..._hqdefault.jpg` | Video thumbnail: the admin base facade | ElRichMC, "EliteCraft 2 Ep 14, La base del administrador", https://www.youtube.com/watch?v=oj-qAh5RVW4 |
| `elrichmc_ep14_storyboard_00-04min.jpg`, `_04-08min.jpg`, `_20-24min.jpg`, `_28-32min.jpg` | YouTube storyboard sheets (5×5 frames, 160×90 each, about 10 s apart): tour, chest hall, library, exterior | same video (YouTube storyboard `L2` sheets; the signed URLs expire, so re-extract them from the watch page's `playerStoryboardSpecRenderer`) |
| `varuna_ernmore_hero_render.jpg` | Ernmore Citadel hero render: castle crowning a rock needle, cathedral face, village | Varuna (build), Sedovtop1st (renders), https://varunabuilds.com/ernmore |
| `varuna_ernmore_cathedral_face.jpg` | The cathedral carved into the rock face | same |
| `varuna_ernmore_interior_hall.jpg` | Interior hall: arches, chandeliers, planters | same |
| `varuna_ernmore_sunset_render.jpg` | Sunset render: warm roofs on a cool body | same |
| `pmc_gothic_cathedral_360_17133823.jpg` | 360-block-tall Gothic cathedral (Cologne/Amiens/Beauvais) in a formal garden, iso | Planet Minecraft, "Gothic Cathedral 350+ blocks tall, with full interior", https://www.planetminecraft.com/project/gothic-cathedral-350-blocks-tall-with-full-interior/ |
| `pmc_gothic_cathedral_360_17133827.jpg` | Same cathedral, apse end: buttress and pinnacle forest | same |
| `opus55_tidewater_voxel_diorama.jpg` | Opus 5.5 "Operation Tidewater" voxel diorama (4 h autonomous run, 65 commits) | Nipale-ai, https://github.com/Nipale-ai/opus-5-5-overnight-builds |

```sh
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
curl -o elrichmc_elitecraft2_ep14_maxresdefault.jpg https://i.ytimg.com/vi/oj-qAh5RVW4/maxresdefault.jpg
curl -o elrichmc_elitecraft2_ep14_hqdefault.jpg     https://i.ytimg.com/vi/oj-qAh5RVW4/hqdefault.jpg
curl -A "$UA" -o pmc_gothic_cathedral_360_17133823.jpg https://static.planetminecraft.com/files/image/minecraft/project/2023/496/17133823_l.jpg
curl -A "$UA" -o pmc_gothic_cathedral_360_17133827.jpg https://static.planetminecraft.com/files/image/minecraft/project/2023/496/17133827_l.jpg
curl -o opus55_tidewater_voxel_diorama.jpg https://raw.githubusercontent.com/Nipale-ai/opus-5-5-overnight-builds/main/vorschau-tidewater.jpg
# Varuna renders: open https://varunabuilds.com/ernmore and take the data-src "_rw_600" images (cdn.myportfolio.com/8d0ed7b2...)
#   7abd367f-... -> hero, 0a8f793d-... -> cathedral face, eceff669-... -> interior hall, 4a3e4a80-... -> sunset
```

## Not here on purpose

- The Ernmore world download (CurseForge project 1085803, All Rights Reserved) was used for measurements only. It is
  kept out of the repo; download it from CurseForge to reproduce research-2 §5.
- Mojang assets are never committed.
