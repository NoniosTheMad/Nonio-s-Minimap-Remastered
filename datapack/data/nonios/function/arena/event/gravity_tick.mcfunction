scoreboard players operation #grav_t nx.arena -= #dt nx.arena
execute if score #grav_t nx.arena matches ..0 run scoreboard players set #grav_t nx.arena 0
execute if score #grav_t nx.arena matches 1.. if score #half nx.arena matches 0 run function nonios:arena/event/gravity_apply with storage nonios:arena config.bounds
