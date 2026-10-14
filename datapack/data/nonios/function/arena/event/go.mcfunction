# Fire the event in storage ev now: announce, run its fn (at its node if it has one). A timed event's fn sets
# #ev_run; the bossbar then shows its remaining time, otherwise it goes away.
scoreboard players set #ev_wait nx.arena 0
scoreboard players set #ev_run nx.arena 0
execute if data storage nonios:arena ev{at:1b} run function nonios:arena/event/announce_at with storage nonios:arena ev
execute unless data storage nonios:arena ev{at:1b} run function nonios:arena/event/announce with storage nonios:arena ev
execute if data storage nonios:arena ev{at:1b} as @e[type=marker,tag=nx.ev_node,limit=1] at @s run function nonios:arena/event/run with storage nonios:arena ev
execute unless data storage nonios:arena ev{at:1b} run function nonios:arena/event/run with storage nonios:arena ev
scoreboard players add #events nx.arena 1
data modify storage nonios:arena last_event set from storage nonios:arena ev.id
execute if score #ev_run nx.arena matches 1.. run return run function nonios:arena/event/bar_run with storage nonios:arena ev
bossbar set nonios:arena/event visible false
