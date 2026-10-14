# as a player whose demo.fx is 1..49: update one layer, a preset, or clear; then re-apply the stack
execute if score @s demo.fx matches 1..5 run scoreboard players operation @s demo.look = @s demo.fx
execute if score @s demo.fx matches 10 run scoreboard players set @s demo.look 0
execute if score @s demo.fx matches 11..12 run scoreboard players operation @s demo.col = @s demo.fx
execute if score @s demo.fx matches 19 run scoreboard players set @s demo.col 0
execute if score @s demo.fx matches 21..22 run scoreboard players operation @s demo.line = @s demo.fx
execute if score @s demo.fx matches 29 run scoreboard players set @s demo.line 0
execute if score @s demo.fx matches 31..31 run scoreboard players operation @s demo.dist = @s demo.fx
execute if score @s demo.fx matches 39 run scoreboard players set @s demo.dist 0
execute if score @s demo.fx matches 41..49 run function demo:fx/preset
function demo:fx/apply
