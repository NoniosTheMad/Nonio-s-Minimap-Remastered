# presets set every layer (49 = clear all)
scoreboard players set @s demo.look 0
scoreboard players set @s demo.col 0
scoreboard players set @s demo.line 0
scoreboard players set @s demo.dist 0
# 41 Cracy Frog
execute if score @s demo.fx matches 41 run scoreboard players set @s demo.col 11
execute if score @s demo.fx matches 41 run scoreboard players set @s demo.dist 31
# 42 Comic book
execute if score @s demo.fx matches 42 run scoreboard players set @s demo.col 12
execute if score @s demo.fx matches 42 run scoreboard players set @s demo.line 21
# 43 Angel
execute if score @s demo.fx matches 43 run scoreboard players set @s demo.look 3
# 44 Neon Reaper
execute if score @s demo.fx matches 44 run scoreboard players set @s demo.look 1
execute if score @s demo.fx matches 44 run scoreboard players set @s demo.line 22
# 45 Star trip
execute if score @s demo.fx matches 45 run scoreboard players set @s demo.look 4
execute if score @s demo.fx matches 45 run scoreboard players set @s demo.dist 31
