# Angel, once a second: the halo comes back if it went (death, rejoin); a mote falls from it
function nonios:dream/pid
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute unless function nonios:class/angel/has_halo run function nonios:class/angel/halo
particle minecraft:end_rod ~ ~2.2 ~ 0.25 0.05 0.25 0.01 1 normal
