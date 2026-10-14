# run the event in tmp.evs[0]: pick a random node if it needs one, announce, run its fn
data modify storage nonios:arena ev set from storage nonios:arena tmp.evs[0]
data modify storage nonios:arena ev.where set value "the Arena"
tag @e[type=marker,tag=nx.ev_node] remove nx.ev_node
execute if data storage nonios:arena ev{at:1b} run tag @e[type=marker,tag=nx.node,sort=random,limit=1] add nx.ev_node
execute if data storage nonios:arena ev{at:1b} unless entity @e[type=marker,tag=nx.ev_node] run return fail
execute as @e[type=marker,tag=nx.ev_node,limit=1] run data modify storage nonios:arena ev.where set from entity @s data.name
execute if data storage nonios:arena ev{at:1b} run function nonios:arena/event/announce_at with storage nonios:arena ev
execute unless data storage nonios:arena ev{at:1b} run function nonios:arena/event/announce with storage nonios:arena ev
execute if data storage nonios:arena ev{at:1b} as @e[type=marker,tag=nx.ev_node,limit=1] at @s run function nonios:arena/event/run with storage nonios:arena ev
execute unless data storage nonios:arena ev{at:1b} run function nonios:arena/event/run with storage nonios:arena ev
scoreboard players add #events nx.arena 1
data modify storage nonios:arena last_event set from storage nonios:arena ev.id
