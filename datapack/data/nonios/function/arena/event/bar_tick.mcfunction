# macro {v = the timer (#ev_wait | #ev_run), n = name function}: the arena loop moves the timer every 10 ticks; in
# between, the bar shows it minus the ticks since then (x #speed), so it drains smoothly. Name only on a new second.
execute store result score #el nx.arena run time query gametime
scoreboard players operation #el nx.arena -= #ev_gt nx.arena
execute if score #el nx.arena matches 11.. run scoreboard players set #el nx.arena 10
scoreboard players operation #el nx.arena *= #speed nx.arena
$scoreboard players operation #ev_vis nx.arena = $(v) nx.arena
scoreboard players operation #ev_vis nx.arena -= #el nx.arena
execute if score #ev_vis nx.arena matches ..0 run scoreboard players set #ev_vis nx.arena 0
execute store result bossbar nonios:arena/event value run scoreboard players get #ev_vis nx.arena
# seconds = ceil(vis / (20 x speed))
scoreboard players operation #div nx.arena = #speed nx.arena
scoreboard players operation #div nx.arena *= #20 nx.arena
scoreboard players operation #sec nx.arena = #ev_vis nx.arena
scoreboard players operation #sec nx.arena += #div nx.arena
scoreboard players remove #sec nx.arena 1
scoreboard players operation #sec nx.arena /= #div nx.arena
execute if score #sec nx.arena = #ev_lsec nx.arena run return 0
scoreboard players operation #ev_lsec nx.arena = #sec nx.arena
execute store result storage nonios:arena ev.sec int 1 run scoreboard players get #sec nx.arena
$function nonios:arena/event/$(n) with storage nonios:arena ev
