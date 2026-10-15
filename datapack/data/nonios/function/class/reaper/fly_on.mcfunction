# as the Reaper, leaving the ground: thinner air (moves at about run speed), no crouch slow-down, no fall build-up
scoreboard players set @s nx.cls_rfly 1
scoreboard players set @s nx.cls_rg -9999
execute store result score @s nx.cls_ry1 run data get entity @s Pos[1] 1000
scoreboard players operation @s nx.cls_ry2 = @s nx.cls_ry1
attribute @s minecraft:air_drag_modifier modifier add nonios:reaper_fly_drag -0.2 add_value
attribute @s minecraft:sneaking_speed modifier add nonios:reaper_fly_sneak 0.7 add_value
