# m2-match
M2 "Playable core": a full match on a generated placeholder map, testable solo.
The game pack does all the work; this demo only adds test buttons (G > "Demo: M2 match") and builds the map on first load.

Game code (datapack/data/nonios/function):
- `game/`: `#state nx.state` 0 lobby / 1 prep / 2 battle / 3 end; `game/tick` runs only the current phase. Start / skip / stop / win / end / to_lobby.
- `team/`: White / Black (teams `white` / `black`), team picker dialog (`/trigger nx.team`), auto-balance at Start (config).
- `admin/`: op unlock `/function nonios:admin` (tag nx.admin), then G > Nonios's Map > Admin panel (`/trigger nx.admin`). Config in storage `nonios:config`.
- `map/config` = every coordinate of the placeholder map (storage `nonios:map`); `map/build` regenerates it (also the map reset after each match).
- `map/walls`: prep barrier walls (barrier blocks + tinted forcefield tiles), dropped at battle start.
- Deaths: `nonios:death` (alive players with `nx.died`): coin bag / killer purse, then `game/death` (stats, last life -> spectator, respawn kit hook `#nonios:kit/respawn`).
- Win check on death events + 1/s in battle: a team loses when its Nexus is gone and nobody of it is alive (husks tagged `nx.dummy` count as alive).
Demo extras: dummies/raiders (`demo:dummy`), destroy own/enemy Nexus (`demo:break`: removes the Barrier, then the obsidian).
