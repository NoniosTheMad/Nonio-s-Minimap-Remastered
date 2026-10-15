# as/at the bound victim: held in place 2 s (a marker pins the spot, bound_tick pulls them back onto it every tick).
# Players see the Reaper's own vision for those 2 s (post effect nonios:reaper; skipped for Reapers, who already have it).
function nonios:class/reaper/unbind
scoreboard players add #bid nx.cls_bid 1
scoreboard players operation @s nx.cls_bid = #bid nx.cls_bid
summon minecraft:marker ~ ~ ~ {Tags:["nx.reaper_pin","nx.new"]}
scoreboard players operation @e[type=marker,tag=nx.new] nx.cls_bid = #bid nx.cls_bid
tag @e[type=marker,tag=nx.new] remove nx.new
execute store result score @s nx.cls_bnd run time query gametime
scoreboard players add @s nx.cls_bnd 40
tag @s add nx.reaper_bound
attribute @s minecraft:movement_speed modifier add nonios:reaper_bind -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier add nonios:reaper_bind -1 add_multiplied_total
execute if entity @s[type=player] unless score @s nx.class matches 1 run posteffect add @s nonios:reaper
title @s[type=player] actionbar {"text":"☠","color":"dark_purple"}
playsound minecraft:entity.wither.shoot player @a ~ ~ ~ 0.8 0.5
playsound minecraft:particle.soul_escape player @a ~ ~ ~ 1.5 0.6
particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.6 0.3 0.03 25
