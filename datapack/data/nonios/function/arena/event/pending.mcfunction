# every arena loop while an event is announced: count down, then fire
scoreboard players operation #ev_wait nx.arena -= #dt nx.arena
execute store result bossbar nonios:arena/event value run scoreboard players get #ev_wait nx.arena
execute if score #ev_wait nx.arena matches ..0 run return run function nonios:arena/event/go
execute if score #half nx.arena matches 0 run function nonios:arena/event/bar_sec
bossbar set nonios:arena/event players @a
