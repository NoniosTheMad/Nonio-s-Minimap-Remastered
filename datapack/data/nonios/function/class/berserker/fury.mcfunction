# health band changed (#l = 0..3): Strength follows it
scoreboard players operation @s nx.cls_blvl = #l nx.cls_tmp
effect clear @s minecraft:strength
execute if score #l nx.cls_tmp matches 1 run effect give @s minecraft:strength infinite 0 true
execute if score #l nx.cls_tmp matches 2 run effect give @s minecraft:strength infinite 1 true
execute if score #l nx.cls_tmp matches 3 run effect give @s minecraft:strength infinite 2 true
execute if score #l nx.cls_tmp matches 2.. run playsound minecraft:entity.ravager.stunned player @a ~ ~ ~ 0.6 1.4
