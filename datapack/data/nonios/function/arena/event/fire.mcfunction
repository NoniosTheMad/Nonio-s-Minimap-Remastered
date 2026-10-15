# Announce the event in tmp.evs[0]: pick its node (if it needs one), then a bossbar counts down event_warn ticks
# (event/pending) and it fires (event/go). #ev_now nx.arena = 1 (event/now) fires it at once instead.
data modify storage nonios:arena ev set from storage nonios:arena tmp.evs[0]
data modify storage nonios:arena ev.where set value "the Arena"
tag @e[type=marker,tag=nx.ev_node] remove nx.ev_node
execute if data storage nonios:arena ev{at:1b} run tag @e[type=marker,tag=nx.node,sort=random,limit=1] add nx.ev_node
execute if data storage nonios:arena ev{at:1b} unless entity @e[type=marker,tag=nx.ev_node] run return fail
execute as @e[type=marker,tag=nx.ev_node,limit=1] run data modify storage nonios:arena ev.where set from entity @s data.name
execute unless data storage nonios:arena ev.bar run data modify storage nonios:arena ev.bar set value "yellow"
execute if score #ev_now nx.arena matches 1 run return run function nonios:arena/event/go
scoreboard players operation #ev_wait nx.arena = #ev_warn nx.arena
execute if score #ev_wait nx.arena matches ..0 run return run function nonios:arena/event/go
function nonios:arena/event/warn with storage nonios:arena ev
