# as + at a node that was just lost (back to neutral): the rune puffs out
data modify storage nonios:arena rx set value {hot:"minecraft:poof",hp:"0 0 0 0.02 1",cp:"0 0 0 0 1",tip:"minecraft:end_rod"}
data modify storage nonios:arena rx.cold set from storage nonios:arena rx.hot
scoreboard players set #lit nx.arena 999
scoreboard players set #tip nx.arena 0
function nonios:arena/rune/view
scoreboard players set @s nx.ar_fx 6
