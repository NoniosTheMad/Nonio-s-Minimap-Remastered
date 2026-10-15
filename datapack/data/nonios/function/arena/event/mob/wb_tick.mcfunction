scoreboard players operation #wb_next nx.arena -= #speed nx.arena
execute if score #wb_waves nx.arena matches 1.. if score #wb_next nx.arena matches ..0 run function nonios:arena/event/mob/wb_wave
scoreboard players operation #wb_t nx.arena -= #speed nx.arena
execute if score #wb_t nx.arena matches ..0 run function nonios:arena/event/mob/wb_end
