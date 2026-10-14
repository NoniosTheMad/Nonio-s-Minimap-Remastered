scoreboard players operation #bounty_t nx.arena -= #dt nx.arena
execute if score #bounty_t nx.arena matches ..0 run tellraw @a [{text:"★ ",color:"red"},{text:"Bounty Hunt is over.",color:"gray"}]
execute if score #bounty_t nx.arena matches ..0 run scoreboard players set #bounty_t nx.arena 0
