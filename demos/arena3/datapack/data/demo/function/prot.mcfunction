# protection on/off (the snapshot is kept; Rebuild map takes a fresh one)
execute store success score #was nx.arena if score #prot nx.arena matches 1
execute if score #was nx.arena matches 1 run scoreboard players set #prot nx.arena 0
execute if score #was nx.arena matches 0 run scoreboard players set #prot nx.arena 1
execute if score #prot nx.arena matches 1 run tellraw @s {"text":"[demo] Arena protection ON.","color":"yellow"}
execute if score #prot nx.arena matches 0 run tellraw @s {"text":"[demo] Arena protection OFF (blocks you break now stay broken until it is back on).","color":"yellow"}
