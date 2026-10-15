# as/at shield: regen reached max HP (or the decay ceiling, nx.hp_cap) -> clamp, bright pulse + chime
scoreboard players operation @s nx.hp = @s nx.hp_cap
scoreboard players set @s nx.regen 0
scoreboard players set @s nx.fx 6
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{scale:[1.5f,1.5f,1.5f]}}
particle minecraft:end_rod ~ ~0.6 ~ 0.5 0.5 0.5 0.02 15
playsound minecraft:block.beacon.power_select block @a ~ ~ ~ 1 1.4
