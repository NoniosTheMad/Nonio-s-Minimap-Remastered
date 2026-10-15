# m4-match
M4 integration: the full match (M2 core + economy) with resource generators, arena nodes/events/lightning and the
Emerald Dream, testable solo. The game pack does all the work; this demo adds test buttons (G > "Demo: M4 match")
and builds the map on first load. Superset of m2-match (buttons 1-14 are the same).

Wiring (game pack):
- `map/config`: per field `gen` (generator, Lv1) and `dream` (portal pad); `arena_cfg` = the 3 arena nodes, rabbit bounds/centre.
  `map/build` places them (`map/gen/generator`, `map/gen/dream_pad`) and rebuilds the nodes (`map/arena_config` + `arena/setup`).
  `#nonios:arena/config` -> `map/arena_hook` re-applies the map's nodes on every load once the map exists.
- Lifecycle: `game/start` -> dreamers woken, `game/reset_world` (generators Lv1 + empty, arena stopped + neutral, portals locked).
  `battle/start` -> `arena/start`; `end/begin` -> `arena/stop`; `to_lobby` -> wake dreamers, arena stop + reset, map rebuild.
  Generators tick only in prep/battle; arena loop only in battle (events, lightning, capture).
- Generator: right-click = collect (pot -> purse, drops jump to you). Sneak-right-click, or right-click with nothing to collect
  = upgrade dialog (own team only; 200 -> Lv2, 500 -> Lv3, from the purse; `/trigger nx.genup`).
- Dream portal (`portal/`): step on your field's end portal frame. Locked: dialog "Open the portal for your team" (1000 coins from the purse,
  `/trigger nx.portal_t`, config `dream_cost`). Open: straight in. Enemy pad: refused. Only in prep/battle.
  Way back: saved spot if still valid (same match, same team, match running), else team spawn (lobby when no match).
  Prep walls only bounce overworld players; the Dream is another dimension, so travellers come back to their pad.
