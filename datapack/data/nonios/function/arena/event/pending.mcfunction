# every arena loop while an event is announced: count down, then fire (event/tick draws the bar every tick)
scoreboard players operation #ev_wait nx.arena -= #dt nx.arena
execute store result score #ev_gt nx.arena run time query gametime
execute if score #ev_wait nx.arena matches ..0 run return run function nonios:arena/event/go
bossbar set nonios:arena/event players @a
