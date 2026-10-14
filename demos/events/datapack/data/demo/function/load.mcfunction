# demo events: the real match on the placeholder map; buttons announce or fire each arena event (G > Demo: Arena events).
# Troll events (frog rain) are on here (demo:arena_cfg).
scoreboard objectives add demo.ev trigger
scoreboard objectives add demo.evc dummy
gamerule spawn_mobs false
gamerule advance_time false
time set noon
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
