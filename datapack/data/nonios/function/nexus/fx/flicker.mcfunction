# as/at shield, HP <=50%: shell dims and shrinks for 2 ticks (unstable); more often at <=25%
scoreboard players set @s nx.fx 3
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,brightness:{sky:2,block:2},transformation:{scale:[1.18f,1.18f,1.18f]}}
particle minecraft:electric_spark ~ ~0.6 ~ 0.6 0.6 0.6 0.1 4
playsound minecraft:block.amethyst_block.step block @a[distance=..16] ~ ~ ~ 0.6 0.5
