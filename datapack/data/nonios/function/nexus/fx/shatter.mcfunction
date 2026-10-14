# as/at shield (macro: shard), barrier hit 0: shell bursts outward, glass shards + sparks, then disappears
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run data merge entity @s {Tags:["nx.shatter"],start_interpolation:0,interpolation_duration:5,brightness:{sky:15,block:15},transformation:{scale:[2.4f,2.4f,2.4f]},item:{components:{"minecraft:item_model":"nonios:nexus_shield_crack3","minecraft:dyed_color":16777215}}}
$particle minecraft:block{block_state:"$(shard)"} ~ ~0.6 ~ 0.6 0.6 0.6 0 120 force
particle minecraft:electric_spark ~ ~0.6 ~ 0.8 0.8 0.8 0.6 80 force
particle minecraft:end_rod ~ ~0.6 ~ 0 0 0 0.25 40 force
playsound minecraft:block.glass.break block @a ~ ~ ~ 2 0.5
playsound minecraft:block.beacon.deactivate block @a ~ ~ ~ 2 0.8
schedule function nonios:nexus/fx/shatter_end 6t append
