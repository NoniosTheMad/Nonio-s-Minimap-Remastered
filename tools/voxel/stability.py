"""World stability: blocks the game will change by itself after placement (random ticks, spread, growth, decay).

    rep = analyze(scene)        {"unstable_soil": n, "spreading": {name: n}, "cells": [...], "fail": bool}
    n = fix_soil(scene)         grass under a full face -> dirt; lit dirt next to grass -> coarse_dirt

Used by `stats` (a FAIL row) and `protect` (refuses to install unless --allow-unstable): on a protected build every
change costs a tile restore forever, and spreading plants creep over the build. Authoring rule: docs/voxel-playbook.md §6.
"""
import numpy as np

from . import blockstate as bs

# name -> why it changes. Matched on the id without namespace; prefix "*" = substring.
SPREADING = {
    "vine": "spreads up, down and sideways",
    "brown_mushroom": "spreads in low light", "red_mushroom": "spreads in low light",
    "mycelium": "spreads onto dirt",
    "cave_vines": "grows down", "twisting_vines": "grows up", "weeping_vines": "grows down",
    "kelp": "grows up", "bamboo": "grows up", "sugar_cane": "grows up", "cactus": "grows up",
    "chorus_flower": "grows", "budding_amethyst": "grows buds", "fire": "spreads, burns", "farmland": "dries to dirt",
    "*sapling": "grows into a tree", "*propagule": "grows into a tree",
}
_TERMINAL_AGE = {"cave_vines": 25, "twisting_vines": 25, "weeping_vines": 25, "kelp": 25}


def _covers(st):
    """Full bottom face (or opaque): grass below it dies; dirt below it can't become grass."""
    from .light import _opacity
    n, p = bs.parse(st)
    return (_opacity(st) >= 15 or (n.endswith("_slab") and p.get("type") != "top")
            or (n.endswith("_stairs") and p.get("half") == "bottom"))


def _spreads(st):
    n, p = bs.parse(st)
    n = n.split(":", 1)[1]
    if n.endswith("_leaves"):
        return "decays (persistent=false)" if p.get("persistent") == "false" else None
    if "copper" in n and not n.startswith(("waxed_", "oxidized_")) and "waxed" not in n:
        return "oxidises (unwaxed copper)"
    for k, why in SPREADING.items():
        if (k[1:] in n) if k.startswith("*") else n == k:
            if n in _TERMINAL_AGE and p.get("age") == str(_TERMINAL_AGE[n]):
                return None
            return why
    return None


def soil_masks(scene):
    names = np.array([bs.name_of(s) for s in scene.palette], object)[scene.idx]
    cov = np.array([_covers(s) for s in scene.palette])[scene.idx]
    above = np.zeros_like(cov); above[:, :-1] = cov[:, 1:]
    grass = names == "minecraft:grass_block"
    dirt = names == "minecraft:dirt"
    near = np.zeros_like(grass)
    for ax, d in ((0, 1), (0, -1), (2, 1), (2, -1), (1, 1), (1, -1)):
        sh = np.roll(grass, d, ax)
        sl = [slice(None)] * 3; sl[ax] = 0 if d == 1 else -1
        sh[tuple(sl)] = False
        near |= sh
    return grass & above, dirt & ~above & near


def analyze(scene):
    dead_grass, greening_dirt = soil_masks(scene)
    why = {s: _spreads(s) for s in scene.palette}
    spreading = {}
    for i, s in enumerate(scene.palette):
        if why[s]:
            n = int((scene.idx == i).sum())
            if n:
                k = f"{bs.name_of(s).split(':', 1)[1]} ({why[s]})"
                spreading[k] = spreading.get(k, 0) + n
    soil = int(dead_grass.sum() + greening_dirt.sum())
    return {"unstable_soil": soil, "grass_under_cover": int(dead_grass.sum()),
            "dirt_next_to_grass": int(greening_dirt.sum()), "spreading": spreading,
            "fail": bool(soil or spreading)}


def fix_soil(scene):
    """grass_block under a full face -> dirt (stable: no light, can't regrow); lit dirt touching grass -> coarse_dirt
    (grass never spreads onto it). Returns the number of cells changed."""
    dead_grass, greening_dirt = soil_masks(scene)
    scene.idx[dead_grass] = scene.id("minecraft:dirt")
    scene.idx[greening_dirt] = scene.id("minecraft:coarse_dirt")
    return int(dead_grass.sum() + greening_dirt.sum())


def format_line(rep):
    if not rep["fail"]:
        return "  stability: PASS (no unstable soil, nothing spreads or decays)"
    sp = ", ".join(f"{k} {v}" for k, v in sorted(rep["spreading"].items(), key=lambda kv: -kv[1]))
    return (f"  stability: FAIL  unstable soil {rep['unstable_soil']} (grass under cover {rep['grass_under_cover']}, "
            f"lit dirt next to grass {rep['dirt_next_to_grass']}; fix_soil() fixes both)"
            + (f"; changes by itself: {sp}" if sp else ""))
