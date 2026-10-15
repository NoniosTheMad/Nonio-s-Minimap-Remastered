# Shift + right-click the Frog Tongue (shares its cooldown): RIBBIT. Wind bursts all around the frog (it gets thrown too, that is the fun).
playsound minecraft:entity.frog.ambient player @a ~ ~ ~ 3 0.5
playsound minecraft:entity.frog.long_jump player @a ~ ~ ~ 2 0.7
title @s actionbar {"text":"RIBBIT!","color":"dark_purple","bold":true}
execute positioned ~ ~0.2 ~ run summon minecraft:wind_charge ^2.5 ^ ^ {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ run summon minecraft:wind_charge ^-2.5 ^ ^ {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ run summon minecraft:wind_charge ^ ^ ^2.5 {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ if predicate nonios:class/coin run summon minecraft:wind_charge ^ ^ ^-2.5 {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ if predicate nonios:class/coin run summon minecraft:wind_charge ^1.8 ^ ^1.8 {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ if predicate nonios:class/coin run summon minecraft:wind_charge ^-1.8 ^ ^1.8 {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ if predicate nonios:class/coin run summon minecraft:wind_charge ^1.8 ^ ^-1.8 {Motion:[0.0,-1.0,0.0]}
execute positioned ~ ~0.2 ~ if predicate nonios:class/coin run summon minecraft:wind_charge ^-1.8 ^ ^-1.8 {Motion:[0.0,-1.0,0.0]}
