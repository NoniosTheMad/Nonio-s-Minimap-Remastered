# as a bound entity (or one about to be bound): free it
attribute @s minecraft:movement_speed modifier remove nonios:reaper_bind
attribute @s minecraft:jump_strength modifier remove nonios:reaper_bind
execute if entity @s[tag=nx.reaper_bound,type=player] unless score @s nx.class matches 1 run posteffect remove @s nonios:reaper
tag @s remove nx.reaper_bound
scoreboard players operation #b nx.cls_tmp = @s nx.cls_bid
execute as @e[type=marker,tag=nx.reaper_pin] if score @s nx.cls_bid = #b nx.cls_tmp run kill @s
scoreboard players reset @s nx.cls_bid
