# as the Reaper: back to normal physics (landed, in a fluid, class gone)
execute unless score @s nx.cls_rfly matches 1 run return 0
scoreboard players set @s nx.cls_rfly 0
attribute @s minecraft:gravity modifier remove nonios:reaper_fly
attribute @s minecraft:air_drag_modifier modifier remove nonios:reaper_fly_drag
attribute @s minecraft:sneaking_speed modifier remove nonios:reaper_fly_sneak
effect clear @s minecraft:slow_falling
