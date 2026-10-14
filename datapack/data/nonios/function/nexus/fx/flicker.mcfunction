# as/at shield, critical HP: shell dims and shrinks for 2 ticks (unstable)
scoreboard players set @s nx.fx 3
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,brightness:{sky:3,block:3},transformation:{scale:[1.33f,1.33f,1.33f]}}
particle minecraft:electric_spark ~ ~0.6 ~ 0.6 0.6 0.6 0.1 4
