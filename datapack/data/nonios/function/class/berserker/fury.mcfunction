# health band changed (#l = 0..3: >75 / <=75 / <=50 / <=25 %): the lower, the harder it hits and the more it steals,
# the less it shrugs off. Resistance IV/III/II/II, Strength -/I/II/III, axe +0/+1/+2/+3 (lifesteal: berserker/lifesteal).
scoreboard players operation @s nx.cls_blvl = #l nx.cls_tmp
effect clear @s minecraft:strength
effect clear @s minecraft:resistance
attribute @s minecraft:attack_damage modifier remove nonios:berserk_fury
execute if score #l nx.cls_tmp matches 0 run effect give @s minecraft:resistance infinite 3 true
execute if score #l nx.cls_tmp matches 1 run effect give @s minecraft:resistance infinite 2 true
execute if score #l nx.cls_tmp matches 2.. run effect give @s minecraft:resistance infinite 1 true
execute if score #l nx.cls_tmp matches 1 run effect give @s minecraft:strength infinite 0 true
execute if score #l nx.cls_tmp matches 2 run effect give @s minecraft:strength infinite 1 true
execute if score #l nx.cls_tmp matches 3 run effect give @s minecraft:strength infinite 2 true
execute if score #l nx.cls_tmp matches 1 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 1 add_value
execute if score #l nx.cls_tmp matches 2 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 2 add_value
execute if score #l nx.cls_tmp matches 3 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 3 add_value
execute if score #l nx.cls_tmp matches 2.. run playsound minecraft:entity.ravager.stunned player @a ~ ~ ~ 0.6 1.4
