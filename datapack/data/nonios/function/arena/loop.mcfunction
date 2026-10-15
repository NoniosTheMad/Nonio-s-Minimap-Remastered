# Every 10 ticks while the arena runs. #dt = game ticks elapsed x #speed (timers only; capture runs in real time).
execute unless score #on nx.arena matches 1 run return 0
# in the match the arena only runs during battle (game/battle/start starts it; anything else stops it)
execute if score #map nx.state matches 1 unless score #state nx.state matches 2 run return run function nonios:arena/stop
schedule function nonios:arena/loop 10t replace
scoreboard players operation #dt nx.arena = #speed nx.arena
scoreboard players operation #dt nx.arena *= #10 nx.arena
# #ph = ticks since this capture check (arena/rune slides bars and runes); bonus effects once per second (#half = 0)
scoreboard players set #ph nx.arena 0
scoreboard players add #half nx.arena 1
execute if score #half nx.arena matches 2.. run scoreboard players set #half nx.arena 0
# nodes; the bonuses held right now are recounted on the way (generator/loop reads #regrow_<team>)
function nonios:arena/bonus/zero
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/node/tick
execute if score #half nx.arena matches 0 run function nonios:arena/bonus/second
# events: announced first (countdown bossbar), then fired; timed ones count down on the same bar
scoreboard players operation #ev_t nx.arena -= #dt nx.arena
execute if score #ev_t nx.arena matches ..0 run function nonios:arena/event/random
execute if score #ev_wait nx.arena matches 1.. run function nonios:arena/event/pending
execute if score #ev_run nx.arena matches 1.. run function nonios:arena/event/running
execute if score #golden_t nx.arena matches 1.. run function nonios:arena/event/golden_tick
execute if score #frog_t nx.arena matches 1.. run function nonios:arena/event/frog_tick
execute if score #bounty_t nx.arena matches 1.. run function nonios:arena/event/bounty_tick
execute if score #grav_t nx.arena matches 1.. run function nonios:arena/event/gravity_tick
# random-entry gates, regrowing core, centre generator
execute if score #gon nx.arena matches 1 run function nonios:arena/gate/loop
execute if score #core nx.arena matches 1 run function nonios:arena/core/loop
execute if score #cgen nx.arena matches 1 run function nonios:arena/cgen/loop
# lightning
execute if score #lt_on nx.arena matches 1 run function nonios:arena/lightning/loop
