# enchantment nonios:class/berserk_lust (post_attack, direct melee hit): as the Berserker. Heals 2 hearts,
# at most once per 1.5 s (fast swings don't stack).
execute store result score #now nx.cls_tmp run time query gametime
scoreboard players operation #d nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #d nx.cls_tmp -= @s nx.cls_heal
execute if score #d nx.cls_tmp matches 0..29 run return 0
scoreboard players operation @s nx.cls_heal = #now nx.cls_tmp
effect give @s minecraft:instant_health 1 0 true
particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 3
