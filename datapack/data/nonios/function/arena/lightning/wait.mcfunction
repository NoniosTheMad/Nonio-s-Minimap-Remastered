# no rabbit: count down to its (re)spawn
scoreboard players operation #lt_rt nx.arena -= #dt nx.arena
execute if score #lt_rt nx.arena matches ..0 run function nonios:arena/lightning/spawn with storage nonios:arena config.center
