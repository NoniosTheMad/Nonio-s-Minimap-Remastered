# Fire one event from config.events, picked by weight. Restarts the event timer.
scoreboard players operation #ev_t nx.arena = #ev_every nx.arena
execute unless score #wsum nx.arena matches 1.. run return 0
scoreboard players set #r nx.arena 1
data modify storage nonios:arena tmp.roll set value {}
execute store result storage nonios:arena tmp.roll.max int 1 run scoreboard players get #wsum nx.arena
execute if score #wsum nx.arena matches 2.. run function nonios:arena/event/roll with storage nonios:arena tmp.roll
data modify storage nonios:arena tmp.evs set from storage nonios:arena config.events
function nonios:arena/event/pick_next
