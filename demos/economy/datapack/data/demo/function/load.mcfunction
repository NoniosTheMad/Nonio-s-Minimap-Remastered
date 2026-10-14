# demo economy: the real game (nonios:) runs match, bank and rewards; this pack only adds solo-test buttons (G > Demo: Economy).
scoreboard objectives add demo.ec trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
