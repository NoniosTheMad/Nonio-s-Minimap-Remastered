"""Reaper vs Warrior 1v1 melee duel, tick by tick (#135 / #137: the Reaper should win ~50% against a Warrior when 60-70% of
the Warrior's swings land on it, the particles around it making it harder to hit).

Numbers are read from src/classes.json (Reaper scythe and pumpkin, Warrior kit for each level), with vanilla 26.x combat on top:
- Attack damage = 1 (player base) + the weapon modifier. Cooldown = ceil(20 / attack_speed) ticks. Both players swing at
  full charge, and a miss still resets the charge.
- Armour: dmg * (1 - clamp(max(armor/5, armor - 4*dmg/(toughness+8)), 0, 20)/25).
- Hurt invulnerability lasts 20 ticks. In the last 10 of them, only damage above the previous (pre-armour) hit gets
  through, and only the difference is dealt.
- Reaper (#137 kit):
  - Fire Aspect I: 4 s burn, 1 damage per second, ignores armour.
  - Regeneration I: +1 HP every 50 ticks. No food regen.
  - Souls:
    - heal: 2 hearts. Spent when the Reaper is at 5 HP or less; the 0.25 s use delays its next swing by 5 ticks.
    - bind (lantern): the Warrior is pinned for 2 s. The Reaper steps just out of the Warrior's reach (its own reach is 3.6
      against 3.0), so the Warrior can't land a swing for those 40 ticks. 5 s cooldown.
    - The policy is the better of "heal only" and "bind once at the start, heal with the rest".
  - Reach assumption: the extra 0.6 blocks gives the Reaper the opening swing (the Warrior's first swing comes 3-10 ticks
    later), and 10% of the Warrior's swings fall short (spacing). Both come on top of the 60/70% hit rate.
- Not modelled: slowness on hit, knockback, flight, the bow, the shield, and the kill rewards (8 s invisible, 3 s
  untouchable). The kill rewards are what pay for the price, and they snowball across fights, not inside one.

  python tools/sim/reaper_vs_warrior.py [--n 10000] [--scan]
"""
import argparse
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SWORD = {"minecraft:stone_sword": (4, 1.6), "minecraft:iron_sword": (5, 1.6), "minecraft:diamond_sword": (6, 1.6)}
ARMOR = {"chainmail": (1, 5, 4, 2), "iron": (2, 6, 5, 2), "diamond": (3, 8, 6, 3)}
TOUGH = {"chainmail": 0, "iron": 0, "diamond": 2}
REACH_WHIFF = 0.10


def mod(comp, attr):
    return sum(m["amount"] for m in comp.get("minecraft:attribute_modifiers", []) if m["type"] == f"minecraft:{attr}")


def fighters(level, over):
    cls = json.loads((ROOT / "src/classes.json").read_text(encoding="utf-8"))["classes"]
    rp = cls["reaper"]["items"]
    head, sc = rp["head"]["components"], rp["scythe"]["components"]
    r = dict(hp=20 + mod(head, "max_health"), armor=mod(head, "armor"), tough=0, dmg=1 + mod(sc, "attack_damage"),
             speed=4 + mod(sc, "attack_speed"), fire="minecraft:fire_aspect" in sc.get("minecraft:enchantments", {}),
             regen=50, heal=4, bind=40)
    r.update(over)
    r["max"] = r["hp"]
    kit = cls["warrior"]["levels"][str(level)]
    mat = kit["chest"]["id"].split(":")[1].split("_")[0]
    sharp = kit["sword"].get("components", {}).get("minecraft:enchantments", {}).get("minecraft:sharpness", 0)
    wd, ws = SWORD[kit["sword"]["id"]]
    w = dict(hp=20, max=20, armor=sum(ARMOR[mat]), tough=TOUGH[mat] * 4, dmg=1 + wd + (0.5 * sharp + 0.5 if sharp else 0),
             speed=ws, fire=False, regen=0, heal=0, bind=0)
    return r, w


def armored(dmg, armor, tough):
    return dmg * (1 - min(20, max(0, max(armor / 5, armor - 4 * dmg / (tough + 8)))) / 25)


def hurt(f, raw, bypass=False):
    """vanilla LivingEntity.hurt with invulnerability frames; True if it took damage"""
    if f["inv"] > 10:
        if raw <= f["last"]:
            return False
        amt, f["last"] = raw - f["last"], raw
    else:
        amt, f["last"], f["inv"] = raw, raw, 20
    f["hp"] -= amt if bypass else armored(amt, f["armor"], f["tough"])
    return True


def duel(r0, w0, p_hit, souls, bind_first, rng):
    r, w = dict(r0), dict(w0)
    for f in (r, w):
        f.update(inv=0, last=0.0, burn=0, phase=rng.randint(0, 19))
    r["cd"], w["cd"] = math.ceil(20 / r["speed"] - 1e-9), math.ceil(20 / w["speed"] - 1e-9)
    r["next"], w["next"] = 0, rng.randint(3, 10)
    pinned_until, bind_ready = -1, 0
    if bind_first and souls and r["bind"]:
        souls, pinned_until, bind_ready = souls - 1, r["bind"], 100
    for t in range(20 * 180):
        for f in (r, w):
            f["inv"] = max(0, f["inv"] - 1)
        if souls and r["hp"] <= 5 and r["heal"]:
            souls -= 1
            r["hp"] = min(r["max"], r["hp"] + r["heal"])
            r["next"] = max(r["next"], t + 5)
        order = (("r", r, w), ("w", w, r)) if rng.random() < 0.5 else (("w", w, r), ("r", r, w))
        for k, me, foe in order:
            if t < me["next"]:
                continue
            me["next"] = t + me["cd"]
            if k == "w" and (t < pinned_until or rng.random() >= p_hit * (1 - REACH_WHIFF)):
                continue
            if hurt(foe, me["dmg"]) and me["fire"]:
                foe["burn"] = max(foe["burn"], 80)
        for f in (r, w):
            if f["burn"] > 0:
                f["burn"] -= 1
                if (t + f["phase"]) % 20 == 0:
                    hurt(f, 1.0, bypass=True)
            if f["regen"] and t % f["regen"] == f["regen"] - 1 and f["hp"] > 0:
                f["hp"] = min(f["max"], f["hp"] + 1)
        if r["hp"] <= 0 or w["hp"] <= 0:
            if r["hp"] <= 0 and w["hp"] <= 0:
                return rng.random() < 0.5
            return w["hp"] <= 0
    return rng.random() < 0.5


def winrate(n, p_hit, souls=0, level=1, seed=1, **over):
    r, w = fighters(level, over)
    best = 0.0
    for bind_first in ((False, True) if souls else (False,)):
        rng = random.Random(seed)
        best = max(best, sum(duel(r, w, p_hit, souls, bind_first, rng) for _ in range(n)) / n)
    return best


def table(n, rows, hits=(0.6, 0.7), souls=(0, 1, 3)):
    head = "".join(f"  {h:.0%}/{s}s" for h in hits for s in souls)
    print(f"{'Reaper win rate':34s}{head}")
    for label, kw in rows:
        print(f"{label:34s}" + "".join(f"{winrate(n, h, s, **kw):>8.1%}" for h in hits for s in souls))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--scan", action="store_true", help="also try single-number Reaper changes")
    a = ap.parse_args()
    r, w = fighters(1, {})
    print(f"Reaper  hp {r['hp']} armor {r['armor']} dmg {r['dmg']} cd {math.ceil(20 / r['speed'])}t fire {r['fire']} "
          f"regen 1/{r['regen']}t heal {r['heal']}/soul bind {r['bind']}t")
    print(f"Warrior hp {w['hp']} armor {w['armor']} dmg {w['dmg']} cd {math.ceil(20 / w['speed'])}t (level 1)")
    rows = [("current kit vs Warrior L1", {})]
    if a.scan:
        rows += [("+ attack speed -3.1 -> -3.0", {"speed": 1.0}), ("+ bind 2 s -> 1 s", {"bind": 20}),
                 ("+ both", {"speed": 1.0, "bind": 20}), ("+ scythe damage +8 -> +9", {"dmg": 10}),
                 ("+ max health -10 -> -8", {"hp": 12})]
    table(a.n, rows)
    print("vs Warrior L2 (iron, no shield):")
    table(a.n, [("current kit vs Warrior L2", {"level": 2})])


if __name__ == "__main__":
    main()
