# cycle the victim profile used by "Simulate a kill" and by killed dummies (#dummy nx.streak / nx.tier): 0/0 -> 3/1 -> 6/3
scoreboard players add #dummy nx.streak 0
execute if score #dummy nx.streak matches 6.. run scoreboard players set #dummy nx.tier -1
execute if score #dummy nx.streak matches 6.. run scoreboard players set #dummy nx.streak -3
scoreboard players add #dummy nx.streak 3
execute if score #dummy nx.streak matches 3 run scoreboard players set #dummy nx.tier 1
execute if score #dummy nx.streak matches 6 run scoreboard players set #dummy nx.tier 3
execute if score #dummy nx.tier matches ..0 run scoreboard players set #dummy nx.tier 0
tellraw @s [{"text":"[demo] Victim profile: streak ","color":"yellow"},{"score":{"name":"#dummy","objective":"nx.streak"},"color":"red"},{"text":", tier ","color":"yellow"},{"score":{"name":"#dummy","objective":"nx.tier"},"color":"light_purple"}]
