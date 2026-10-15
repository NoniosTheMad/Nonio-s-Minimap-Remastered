# as/at whoever stepped in a Balrog trail: withered (Wither II) until death or milk
execute if predicate nonios:class/withered run return 0
effect give @s minecraft:wither infinite 1
particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 15
playsound minecraft:entity.wither.ambient hostile @a ~ ~ ~ 0.6 1.4
title @s[type=player] actionbar {"text":"☠ The shadow clings to you.","color":"dark_red","italic":true}
