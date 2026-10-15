# weighted pick from config.core_blocks -> storage nonios:arena core_pick {id,w}; #ci nx.arena = its index (0..)
scoreboard players set #r nx.arena 1
data modify storage nonios:arena tmp.roll set value {}
execute store result storage nonios:arena tmp.roll.max int 1 run scoreboard players get #cwsum nx.arena
execute if score #cwsum nx.arena matches 2.. run function nonios:arena/event/roll with storage nonios:arena tmp.roll
data modify storage nonios:arena tmp.cbl set from storage nonios:arena config.core_blocks
scoreboard players set #ci nx.arena 0
function nonios:arena/core/pick_next
