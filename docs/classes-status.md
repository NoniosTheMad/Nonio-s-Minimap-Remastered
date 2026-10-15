# Classes: V2 original vs remaster (status 2026-10-15, branch feat/classes)

Source of truth for definitions: `src/classes.json` (built by `tools/build_classes.py`), hand-written abilities in
`datapack/data/nonios/function/class/<id>/`. V2 behaviour comes from the read-only `../V2.0 - Just substitute thee world`
command blocks (see `docs/v2-gap-inventory.md` section 6). Demos: `classes` (every class, one button each) and `classes2`
(V2 shop classes inside the full M5 match).

Status key: **done** = playable and reviewed by the user. **built** = playable, not yet judged. **new** = remaster-only design.
**planned** = design only.

## Shop classes (bought, lost on death)

| class | price | V2 original | remaster | status |
|---|---|---|---|---|
| Archer | 50 | chain armour, bow, stone tools | Hunter's Bow marks hits (glow 6 s), a quiver that refills 1 arrow / 3 s up to 16 | built (main) |
| Miner | 80 | leather, pickaxe, night vision | night vision + mining grit, Block Pulverizer flask (haste III + glowing 8 s, 45 s cd) | built (main) |
| Tank | 100 | iron + shield | iron + locked shield, +2 hearts, 40% knockback resistance, Ironskin flask | built (main) |
| Ninja | 100 | armour stripped, Chunin Sandals | sandals only: fast, step-up, frost walker, light fall; Genjutsu flask (invisible + fast; never used up, 20 s cooldown) | built (main) |
| Berserker | 120 | strength, speed, regen, armour stripped | #84: light axe (3 dmg, attack speed 8), axe out = Resistance IV + armour 0 + speed + no knockback; Strength I/II/III at <=75/50/25 % HP; hit = +2 hearts lifesteal (once per 1.5 s); no natural/food regeneration (food held at 17 by hidden Hunger, Saturation effects stripped) | built |
| **Champion** | 150 | none | grows with player kills while undefeated (see below) | **new**, built |
| Reaper | 200 | pumpkin, scythe, permanent invisibility + speed II, 3 s resistance V per kill | see below (#70/#71 rework) | built |
| Monster | 1800 | Monster Transformation (300) / Skull (1800): devour on kill, hunger | +10 hearts, bigger, faster, claws with short reach, 80% knockback resistance; every kill devoured (strength, speed, heal) | built (main) |
| Balrog | 10000 | jump boost, fire res., lava trail (bad luck, cursed, wither II), wall climb, custom sound | 150 hearts, armour 20, fireproof, cannot jump, climbs walls, 5.5-block lash at 0.6 hits/s, own aura hidden from itself, wither trail. No custom sound yet (needs audio) | built (main) |
| Cracy Frog | free (3 "are you sure?") | frog head, Frog Skin, Frog Spring boots, Magic Broom | see below ("annoying" rework) | built |

### Reaper (rework #70/#71)
- Scythe: 2-heart lifesteal per swing and Slowness I for 3 s on hit.
- Kill: +1 soul (max 5), 4 s invisibility, 8 s Resistance V. Resistance doesn't refresh while it's active, so kills can't chain it.
- Invisible means invisible: the pumpkin and the scythe models are hidden too (`item_model` air) and come back afterwards.
- Right-click the charged scythe (it glints) to burst the souls. With no souls you get "No souls" and the scythe is never consumed.
- Flight in the air:
  - Holding Space rises, Shift sinks, and holding nothing hovers.
  - Horizontal speed is about walk/sprint (5.2 / 6.7 b/s).
  - It can only rise within 10 blocks of the ground. Higher than that it sinks slowly.
  - No fall damage. Water, lava or landing ends the flight.

### Cracy Frog ("the definition of annoying", #73)
- Frog Tongue, right-click (0.35 s wind-up, 7 s cooldown):
  - The tongue travels 1.5 blocks/tick, up to 12 blocks. You can see it and dodge it.
  - When it catches someone, a wind burst throws them up and toward the frog while the frog springs backwards.
  - Players take fall damage on landing: blocks fallen from the peak minus 3, capped at 3 hearts.
  - Counters: water, lava, cobweb, slow falling and feather falling. Allies are ignored, and the victim is immune to tongues for 3 s.
- Shift + right-click: RIBBIT (the old wind bursts all around). It shares the cooldown.
- Melee hit: a random chaos effect (yeet, levitate, spin, nausea, sticky).
- Magic Broom: hold to fly by pitch, 3 s fuel. Frog Legs: big jumps, 12 blocks of safe fall.

### Champion (new, #74)
- Kit: iron armour locked on, a golden Champion's Crown, Champion's Blade (iron sword), stone tools, cobblestone, beef.
- Each player kill while alive gives +1 heart, +0.5 attack damage and an instant heal, up to 5 kills.
- At 3 kills it glows for everyone and its crown sparkles. Everyone sees "<name> ⚔ 3" at 3 and "⚔ 5" at 5.
- Bounty: whoever kills a Champion with 3+ kills gets 10 coins per kill.
- Death ends the run. It's a shop class, so it's lost and starts again from 0.

## Basic class (re-applied on every respawn)

| class | V2 | remaster | status |
|---|---|---|---|
| Warrior | "Automatic Kits" I/II/III from team offerings | chainmail / iron + shield / diamond + Gardna's Shield, by team level | built; stays basic and cheap, no personal levelling (that is the Champion now) |

## Never implemented in V2 (names only, on the V2 menu and planned-class signs)

Paladin 300, Death Knight 500, Titan 1500, Destroyer 2000, Guardian Angel 5000. V2 has no design for any of them.

## Open questions
- Warrior keeps its kit by **team** level, the V2 offering upgrade. Is that fine, or should Warrior be flat (one kit only)?
- Champion: price 150 and bounty 10 coins/kill are guesses. Should a downed Champion's kill tier rise with its level?
- Should the five unbuilt V2 classes get remaster designs, and in which order?
- Should invisible players glow (the V2 `weakInv` rule), except the Reaper and Ninja?
