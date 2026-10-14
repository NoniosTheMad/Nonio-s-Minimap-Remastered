# as a player on a gate pad: in at the active slot's landing point; every player hears it (V2)
execute unless entity @e[type=marker,tag=nx.aslot_on] run return 0
function nonios:arena/gate/go with entity @e[type=marker,tag=nx.aslot_on,limit=1] data.land
function nonios:arena/gate/sound with storage nonios:arena config.gate
scoreboard players add #g_in nx.arena 1
