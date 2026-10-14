# as/at shield: HP crossed 75/50/25%. Down = more cracks, redder, smaller; up (regen) = cracks mend.
execute if score #stage nx.const > @s nx.stage run playsound minecraft:block.glass.break block @a ~ ~ ~ 1.4 0.6
execute if score #stage nx.const > @s nx.stage run particle minecraft:electric_spark ~ ~0.6 ~ 0.7 0.7 0.7 0.3 40
execute if score #stage nx.const < @s nx.stage run playsound minecraft:block.amethyst_block.resonate block @a ~ ~ ~ 1.5 1.2
scoreboard players operation @s nx.stage = #stage nx.const
$execute if score @s nx.stage matches 0 store result score @s nx.col run data get storage nonios:nexus team.$(team).col[0]
$execute if score @s nx.stage matches 1 store result score @s nx.col run data get storage nonios:nexus team.$(team).col[1]
$execute if score @s nx.stage matches 2 store result score @s nx.col run data get storage nonios:nexus team.$(team).col[2]
$execute if score @s nx.stage matches 3 store result score @s nx.col run data get storage nonios:nexus team.$(team).col[3]
execute if score @s nx.stage matches 0 as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data modify entity @s item.components."minecraft:item_model" set value "nonios:nexus_shield"
execute if score @s nx.stage matches 1 as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data modify entity @s item.components."minecraft:item_model" set value "nonios:nexus_shield_crack1"
execute if score @s nx.stage matches 2 as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data modify entity @s item.components."minecraft:item_model" set value "nonios:nexus_shield_crack2"
execute if score @s nx.stage matches 3 as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data modify entity @s item.components."minecraft:item_model" set value "nonios:nexus_shield_crack3"
execute if score @s nx.fx matches 0 run function nonios:nexus/fx/rest
