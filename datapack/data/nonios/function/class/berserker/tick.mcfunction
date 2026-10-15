# Berserker, every tick.
# Nothing heals a Berserker but its own lifesteal (#89): food, saturation, regeneration, potions, beacons...
# (berserker/guard also feeds Rage from damage taken: berserker/hurt)
function nonios:class/berserker/guard
# Rage (nx.cls_brg 0..100, #93) cools 10 / s once 3 s pass without a hit dealt or taken
execute store result score #now nx.cls_tmp run time query gametime
execute if score @s nx.cls_brg matches 1.. run function nonios:class/berserker/cool
# Fury = the BattleAxe in hand (the axe itself zeroes armour, adds speed and knockback immunity)
execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{nx_item:"berserker_axe"}] run return run function nonios:class/berserker/calm
execute unless entity @s[tag=nx.cls_rage] run function nonios:class/berserker/rage
# Rage tier 0..4 (every 25): the angrier, the harder and faster it hits and the more it steals, the less it shrugs off
scoreboard players operation #l nx.cls_tmp = @s nx.cls_brg
scoreboard players operation #l nx.cls_tmp /= #25 nx.cls_tmp
execute unless score #l nx.cls_tmp = @s nx.cls_blvl run function nonios:class/berserker/fury
# the rage shows: red mist thickening with the tier
scoreboard players operation #p nx.cls_tmp = #now nx.cls_tmp
scoreboard players operation #p nx.cls_tmp %= #5 nx.cls_tmp
execute if score #p nx.cls_tmp matches 0 if score @s nx.cls_blvl matches 1.. run function nonios:class/berserker/mist
