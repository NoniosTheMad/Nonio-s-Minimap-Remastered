# Rage tier changed (#l = 0..4, every 25 Rage). Tier 0..4:
#   Resistance IV / III / II / I / none, axe damage +0 / +1 / +2 / +3 / +4, attack speed 5 / 5.75 / 6.5 / 7.25 / 8
#   (lifesteal: berserker/lifesteal)
scoreboard players operation @s nx.cls_blvl = #l nx.cls_tmp
effect clear @s minecraft:resistance
attribute @s minecraft:attack_damage modifier remove nonios:berserk_fury
attribute @s minecraft:attack_speed modifier remove nonios:berserk_haste
execute if score #l nx.cls_tmp matches 0 run effect give @s minecraft:resistance infinite 3 true
execute if score #l nx.cls_tmp matches 1 run effect give @s minecraft:resistance infinite 2 true
execute if score #l nx.cls_tmp matches 2 run effect give @s minecraft:resistance infinite 1 true
execute if score #l nx.cls_tmp matches 3 run effect give @s minecraft:resistance infinite 0 true
execute if score #l nx.cls_tmp matches 1 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 1 add_value
execute if score #l nx.cls_tmp matches 2 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 2 add_value
execute if score #l nx.cls_tmp matches 3 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 3 add_value
execute if score #l nx.cls_tmp matches 4 run attribute @s minecraft:attack_damage modifier add nonios:berserk_fury 4 add_value
execute if score #l nx.cls_tmp matches 1 run attribute @s minecraft:attack_speed modifier add nonios:berserk_haste 0.75 add_value
execute if score #l nx.cls_tmp matches 2 run attribute @s minecraft:attack_speed modifier add nonios:berserk_haste 1.5 add_value
execute if score #l nx.cls_tmp matches 3 run attribute @s minecraft:attack_speed modifier add nonios:berserk_haste 2.25 add_value
execute if score #l nx.cls_tmp matches 4 run attribute @s minecraft:attack_speed modifier add nonios:berserk_haste 3 add_value
execute if score #l nx.cls_tmp matches 4 run playsound minecraft:entity.ravager.roar player @a ~ ~ ~ 0.8 1.1
execute if score #l nx.cls_tmp matches 2..3 run playsound minecraft:entity.ravager.stunned player @a ~ ~ ~ 0.5 1.4
