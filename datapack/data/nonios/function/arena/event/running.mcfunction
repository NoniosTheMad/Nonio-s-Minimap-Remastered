# every arena loop while a timed event runs: count down (event/tick draws the bar every tick)
scoreboard players operation #ev_run nx.arena -= #dt nx.arena
execute store result score #ev_gt nx.arena run time query gametime
execute if score #ev_run nx.arena matches ..0 run bossbar set nonios:arena/event visible false
