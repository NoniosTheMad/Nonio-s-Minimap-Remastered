execute store success score #was demo.evc unless score #trolls demo.evc matches 0
execute if score #was demo.evc matches 1 run scoreboard players set #trolls demo.evc 0
execute if score #was demo.evc matches 0 run scoreboard players set #trolls demo.evc 1
function demo:recfg
execute if score #trolls nx.arena matches 1 run tellraw @s {"text":"[demo] Troll events ON (frog rain can come up at random).","color":"yellow"}
execute if score #trolls nx.arena matches 0 run tellraw @s {"text":"[demo] Troll events OFF (the match default).","color":"yellow"}
