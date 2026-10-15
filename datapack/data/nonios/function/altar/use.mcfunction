# as/at a player who right-clicked an altar: whose altar is it (within 6 blocks), then offer
scoreboard players set #t nx.altar 0
execute if entity @e[type=interaction,tag=nx.altar_npc,tag=nx.white,distance=..6] run scoreboard players set #t nx.altar 1
execute if entity @e[type=interaction,tag=nx.altar_npc,tag=nx.black,distance=..6] run scoreboard players set #t nx.altar 2
execute if score #t nx.altar matches 0 run return 0
execute if score #t nx.altar matches 1 unless entity @s[team=white] run return run title @s actionbar {text:"It does not answer to you.",color:"red"}
execute if score #t nx.altar matches 2 unless entity @s[team=black] run return run title @s actionbar {text:"It does not answer to you.",color:"red"}
execute unless score #state nx.state matches 1..2 run return run title @s actionbar {text:"The altar is silent.",color:"gray"}
execute if score #t nx.altar matches 1 run function nonios:altar/offer {team:"white"}
execute if score #t nx.altar matches 2 run function nonios:altar/offer {team:"black"}
