# demo shop3: the real game (nonios:) with shop v3, the gear helper (hotbar slots) and arrow damage on the Nexus barrier;
# this pack only adds solo-test buttons (G > Demo: Shop v3).
scoreboard objectives add demo.shop3 trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
