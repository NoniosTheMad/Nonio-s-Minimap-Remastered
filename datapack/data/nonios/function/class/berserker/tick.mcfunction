# Berserker, every tick.
# Food never heals: natural regeneration needs food >= 18, so above 17 a hidden Hunger 255 burns it back down
# (a fresh steak can still leak ~1-3 HP through saturation before it is gone).
execute if predicate nonios:class/berserker/fed run effect clear @s minecraft:saturation
execute store result score #f nx.cls_tmp run data get entity @s foodLevel
execute if score #f nx.cls_tmp matches 18.. run effect give @s minecraft:hunger 1 255 true
execute if score #f nx.cls_tmp matches ..17 if predicate nonios:class/berserker/hungry run effect clear @s minecraft:hunger
# Fury = the BattleAxe in hand (the axe itself zeroes armour, adds speed and knockback immunity)
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{nx_item:"berserker_axe"}] run return run function nonios:class/berserker/calm
execute unless entity @s[tag=nx.cls_rage] run function nonios:class/berserker/rage
# the lower the health, the harder it hits: Strength I/II/III at <=75/50/25 % of max health
execute store result score #h nx.cls_tmp run data get entity @s Health 100
execute store result score #m nx.cls_tmp run attribute @s minecraft:max_health get
scoreboard players operation #h nx.cls_tmp /= #m nx.cls_tmp
scoreboard players set #l nx.cls_tmp 0
execute if score #h nx.cls_tmp matches ..75 run scoreboard players set #l nx.cls_tmp 1
execute if score #h nx.cls_tmp matches ..50 run scoreboard players set #l nx.cls_tmp 2
execute if score #h nx.cls_tmp matches ..25 run scoreboard players set #l nx.cls_tmp 3
execute unless score #l nx.cls_tmp = @s nx.cls_blvl run function nonios:class/berserker/fury
