# Berserker, every tick.
# Nothing heals a Berserker but its own lifesteal (#89): food, saturation, regeneration, potions, beacons...
function nonios:class/berserker/guard
# Fury = the BattleAxe in hand (the axe itself zeroes armour, adds speed and knockback immunity)
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{nx_item:"berserker_axe"}] run return run function nonios:class/berserker/calm
execute unless entity @s[tag=nx.cls_rage] run function nonios:class/berserker/rage
# the lower the health, the wilder: band 0..3 at >75 / <=75 / <=50 / <=25 % of max health (berserker/fury)
scoreboard players operation #h nx.cls_tmp = @s nx.cls_bhp
scoreboard players operation #h nx.cls_tmp /= #mx nx.cls_tmp
scoreboard players set #l nx.cls_tmp 0
execute if score #h nx.cls_tmp matches ..75 run scoreboard players set #l nx.cls_tmp 1
execute if score #h nx.cls_tmp matches ..50 run scoreboard players set #l nx.cls_tmp 2
execute if score #h nx.cls_tmp matches ..25 run scoreboard players set #l nx.cls_tmp 3
execute unless score #l nx.cls_tmp = @s nx.cls_blvl run function nonios:class/berserker/fury
