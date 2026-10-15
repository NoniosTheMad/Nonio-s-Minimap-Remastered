# demo team2 (feat/team-v2): demos/full + offering altar, spawn defense, Emerald Talisman, Dragon Skull joke, lightning
# admin switch, recipes at start, prep walls underground. Solo-test buttons: G > Demo: Team altar.
scoreboard objectives add demo.team2 trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
