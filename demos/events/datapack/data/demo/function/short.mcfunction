execute store success score #was demo.evc if score #short demo.evc matches 1
execute if score #was demo.evc matches 1 run scoreboard players set #short demo.evc 0
execute if score #was demo.evc matches 0 run scoreboard players set #short demo.evc 1
function demo:recfg
execute if score #short demo.evc matches 1 run tellraw @s {"text":"[demo] Warning 5 s before each event.","color":"yellow"}
execute if score #short demo.evc matches 0 run tellraw @s {"text":"[demo] Warning 30 s before each event (the match default).","color":"yellow"}
