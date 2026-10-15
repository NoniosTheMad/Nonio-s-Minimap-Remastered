tag @s remove nx.reform
data merge entity @s {start_interpolation:0,interpolation_duration:14,transformation:{scale:[1.4f,1.4f,1.4f]}}
particle minecraft:reverse_portal ~ ~ ~ 0.9 0.9 0.9 0.02 80
particle minecraft:end_rod ~ ~ ~ 0.9 0.9 0.9 0 20
playsound minecraft:block.beacon.activate block @a ~ ~ ~ 1.5 1.2
playsound minecraft:block.respawn_anchor.charge block @a ~ ~ ~ 1 1.2
