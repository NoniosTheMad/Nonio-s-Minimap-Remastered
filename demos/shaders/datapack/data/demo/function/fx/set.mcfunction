# as a player whose demo.fx is 1..49: update one layer, a preset, or clear; then re-apply the stack
# a 'No X' button while a preset is on removes the whole preset (presets read as one effect)
execute if score @s demo.pre matches 1.. if score @s demo.fx matches 10 run function demo:fx/unpreset
execute if score @s demo.pre matches 1.. if score @s demo.fx matches 19 run function demo:fx/unpreset
execute if score @s demo.pre matches 1.. if score @s demo.fx matches 29 run function demo:fx/unpreset
execute if score @s demo.pre matches 1.. if score @s demo.fx matches 39 run function demo:fx/unpreset
# any single-layer click turns a preset into a custom stack
execute if score @s demo.fx matches 1..39 run scoreboard players set @s demo.pre 0
# demo.look: clicking the active effect again turns it off
scoreboard players set #tog demo.st 0
execute if score @s demo.fx matches 1..5 if score @s demo.look = @s demo.fx store success score #tog demo.st run scoreboard players set @s demo.look 0
execute if score #tog demo.st matches 0 if score @s demo.fx matches 1..5 run scoreboard players operation @s demo.look = @s demo.fx
execute if score @s demo.fx matches 10 run scoreboard players set @s demo.look 0
# demo.col: clicking the active effect again turns it off
scoreboard players set #tog demo.st 0
execute if score @s demo.fx matches 11..12 if score @s demo.col = @s demo.fx store success score #tog demo.st run scoreboard players set @s demo.col 0
execute if score #tog demo.st matches 0 if score @s demo.fx matches 11..12 run scoreboard players operation @s demo.col = @s demo.fx
execute if score @s demo.fx matches 19 run scoreboard players set @s demo.col 0
# demo.line: clicking the active effect again turns it off
scoreboard players set #tog demo.st 0
execute if score @s demo.fx matches 21..22 if score @s demo.line = @s demo.fx store success score #tog demo.st run scoreboard players set @s demo.line 0
execute if score #tog demo.st matches 0 if score @s demo.fx matches 21..22 run scoreboard players operation @s demo.line = @s demo.fx
execute if score @s demo.fx matches 29 run scoreboard players set @s demo.line 0
# demo.dist: clicking the active effect again turns it off
scoreboard players set #tog demo.st 0
execute if score @s demo.fx matches 31..31 if score @s demo.dist = @s demo.fx store success score #tog demo.st run scoreboard players set @s demo.dist 0
execute if score #tog demo.st matches 0 if score @s demo.fx matches 31..31 run scoreboard players operation @s demo.dist = @s demo.fx
execute if score @s demo.fx matches 39 run scoreboard players set @s demo.dist 0
execute if score @s demo.fx matches 41..49 run function demo:fx/preset
function demo:fx/apply
