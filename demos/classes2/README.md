# classes2
The remaining V2 shop classes (Archer 50, Miner 80, Tank 100, Ninja 100, Berserker 120, Monster 1800, Balrog 10000) on the
class framework, inside the full M5 match. Copy of `demos/m5-classes` (trigger `demo.c2`, dialog `demo:c2`): buttons 1-34 are
the same, 35-41 give each new class for free, 42-45 are target dummies, a mob wave, reset cooldowns, clear mobs.

Game-pack side (all from `src/classes.json` via `tools/build_classes.py`, hand-written abilities in `function/class/<id>/`):
- New item slot `supply`: plain kit items (tools, blocks, food) given once on apply, never re-checked.
- New hook `second` (once per second per class holder), dispatched by `class/gen/second` from `class/second`.
- Consumable flasks (Miner Pulverizer, Tank Ironskin, Ninja Genjutsu) use the existing use advancement + cooldown + restock path.
- Enchantments (restart after changes): archer_mark, miner_grit, tank_bulwark, ninja_sandals, monster_hunger, balrog_aura.
- Balrog trail = markers `nx.bal_trail` (life `nx.cls_ttl`), ticked from `class/tick`; Archer quiver timer `nx.cls_quiv`.
- `advancement/class/monster_kill` (player_killed_entity: player or `nx.soul` mob) runs `class/monster/devour`.
