data merge entity @s {start_interpolation:0,interpolation_duration:4,brightness:{sky:15,block:15}}
execute store result entity @s transformation.scale[0] float 0.01 run scoreboard players get #scale nx.const
execute store result entity @s transformation.scale[1] float 0.01 run scoreboard players get #scale nx.const
execute store result entity @s transformation.scale[2] float 0.01 run scoreboard players get #scale nx.const
execute store result entity @s item.components."minecraft:dyed_color" int 1 run scoreboard players get #col nx.const
