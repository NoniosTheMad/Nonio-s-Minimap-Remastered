# Berserker, once a second. With the BattleAxe in hand the fury is on: the axe itself zeroes armour and toughness,
# adds speed and knockback immunity (mainhand attributes); here: Regeneration III while it lasts.
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{nx_item:"berserker_axe"}] run return run tag @s remove nx.cls_rage
effect give @s minecraft:regeneration 3 2 true
particle minecraft:angry_villager ~ ~2 ~ 0.3 0.2 0.3 0 1
execute if entity @s[tag=nx.cls_rage] run return 0
tag @s add nx.cls_rage
playsound minecraft:entity.ravager.roar player @a ~ ~ ~ 0.7 1.3
