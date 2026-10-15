# enchantment nonios:class/berserk_lust (post_attack, direct melee hit): as the Berserker.
# Each hit feeds Rage (+5, at most every 5 ticks so spam-clicking does not count), then steals life;
# the angrier (tier nx.cls_blvl 0..4), the more often and the more: 2 hearts per 2 s / 1.5 s / 1 s, 4 hearts per 1.5 s / 1 s.
execute store result score #now nx.cls_tmp run time query gametime
scoreboard players operation #d nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #d nx.cls_tmp -= @s nx.cls_brh
execute unless score #d nx.cls_tmp matches 0..4 run function nonios:class/berserker/fed
scoreboard players operation #d nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #d nx.cls_tmp -= @s nx.cls_heal
execute if score @s nx.cls_blvl matches ..0 if score #d nx.cls_tmp matches 0..39 run return 0
execute if score @s nx.cls_blvl matches 1 if score #d nx.cls_tmp matches 0..29 run return 0
execute if score @s nx.cls_blvl matches 2 if score #d nx.cls_tmp matches 0..19 run return 0
execute if score @s nx.cls_blvl matches 3 if score #d nx.cls_tmp matches 0..29 run return 0
execute if score @s nx.cls_blvl matches 4.. if score #d nx.cls_tmp matches 0..19 run return 0
scoreboard players operation @s nx.cls_heal = #now nx.cls_tmp
# a clamp from the guard would swallow the heal: lift it first
execute if score @s nx.cls_bcap matches 1.. run function nonios:class/berserker/uncap
execute if score @s nx.cls_blvl matches ..2 run effect give @s minecraft:instant_health 1 0 true
execute if score @s nx.cls_blvl matches 3.. run effect give @s minecraft:instant_health 1 1 true
# the only heal the guard lets through (berserker/granted, once the effect lands next tick)
execute if score @s nx.cls_blvl matches ..2 run scoreboard players set @s nx.cls_bgr 400
execute if score @s nx.cls_blvl matches 3.. run scoreboard players set @s nx.cls_bgr 800
scoreboard players set @s nx.cls_bgt 3
particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 3
