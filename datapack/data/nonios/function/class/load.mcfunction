# Class framework (DESIGN 2.12): objectives + defaults. Called from nonios:load.
# Definitions: src/classes.json -> python tools/build_classes.py -> class/gen/**, loot_table/class/**, enchantment/class/**.
# current class number (0/unset = none) and the chosen basic class (re-applied on respawn)
scoreboard objectives add nx.class dummy
scoreboard objectives add nx.cls_basic dummy
# argument for class/gen/apply
scoreboard objectives add nx.cls_req dummy
# basic-class upgrade level per team (1-3): #white #black #solo (players without a team)
scoreboard objectives add nx.cls_lvl dummy
# victim tier for the kill bonus (economy kill_bonus/tier reads it): owned by classes, set on apply, 0 without a class
scoreboard objectives add nx.tier dummy
scoreboard objectives add nx.cls_tmp dummy
# Reaper souls / lifesteal gate (gametime of the last heal)
scoreboard objectives add nx.cls_souls dummy
scoreboard objectives add nx.cls_heal dummy
# Cracy Frog broom: fuel (ticks), >0 while right-click is held, forward-impulse gate read by the frog_broom enchantment
scoreboard objectives add nx.cls_fuel dummy
scoreboard objectives add nx.cls_fly dummy
scoreboard objectives add nx.cls_kick dummy
# a consumable class item was used up (survival): give it back next tick
scoreboard objectives add nx.cls_restock dummy
# 1 = class items are given with the alternate cooldown group (demo "reset cooldowns")
scoreboard objectives add nx.cls_cdalt dummy
# rejoin detection (post effects are client state, lost on reconnect)
scoreboard objectives add nx.cls_left minecraft.custom:minecraft.leave_game
# Cracy Frog confirmation chain (dialog buttons) + the step each player reached
scoreboard objectives add nx.cls_ask trigger
scoreboard objectives add nx.cls_askst dummy
execute unless score #white nx.cls_lvl matches 1.. run scoreboard players set #white nx.cls_lvl 1
execute unless score #black nx.cls_lvl matches 1.. run scoreboard players set #black nx.cls_lvl 1
execute unless score #solo nx.cls_lvl matches 1.. run scoreboard players set #solo nx.cls_lvl 1
scoreboard players set #6 nx.cls_tmp 6
function nonios:class/gen/catalog
