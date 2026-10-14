# as/at shield, on a damaging hit (macro: shard): shell flashes white and bulges, glass chips fly, sparks + shield sound
scoreboard players set @s nx.fx 4
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,brightness:{sky:15,block:15},transformation:{scale:[1.55f,1.55f,1.55f]},item:{components:{"minecraft:dyed_color":16777215}}}
$particle minecraft:block{block_state:"$(shard)"} ~ ~0.6 ~ 0.5 0.5 0.5 0 18 force
particle minecraft:electric_spark ~ ~0.6 ~ 0.45 0.45 0.45 0.25 25
particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.4 0.4 0.04 6
playsound minecraft:item.shield.block block @a ~ ~ ~ 1.2 0.7
playsound minecraft:block.amethyst_block.hit block @a ~ ~ ~ 1.5 0.6
