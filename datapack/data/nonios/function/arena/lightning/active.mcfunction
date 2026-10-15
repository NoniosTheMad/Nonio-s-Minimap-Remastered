function nonios:arena/lightning/leash with storage nonios:arena config.bounds
scoreboard players operation #lt_t nx.arena -= #dt nx.arena
execute if score #lt_t nx.arena matches ..0 run function nonios:arena/lightning/strike
