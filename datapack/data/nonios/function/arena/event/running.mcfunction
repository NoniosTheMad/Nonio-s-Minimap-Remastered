scoreboard players operation #ev_run nx.arena -= #dt nx.arena
execute store result bossbar nonios:arena/event value run scoreboard players get #ev_run nx.arena
execute if score #ev_run nx.arena matches ..0 run bossbar set nonios:arena/event visible false
