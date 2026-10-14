# demo m2-match: the real game (nonios:) runs the match; this pack only adds solo-test buttons (G > Demo: M2 match).
scoreboard objectives add demo.m2 trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
