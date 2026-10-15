# stop tracking; 3 s before a tongue can catch this player again
tag @s remove nx.frog_yanked
tag @s remove nx.frog_hooked
attribute @s minecraft:gravity modifier remove nonios:frog_hook
attribute @s minecraft:fall_damage_multiplier modifier remove nonios:frog_hook
tag @s add nx.frog_immune
scoreboard players set @s nx.cls_yk 60
