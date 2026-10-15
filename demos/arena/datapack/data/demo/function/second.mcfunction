# demo HUD: event countdown on the board at spawn
schedule function demo:second 20t replace
scoreboard players operation #div demo.c = #speed nx.arena
scoreboard players operation #div demo.c *= #20 nx.arena
scoreboard players operation #sec demo.c = #ev_t nx.arena
scoreboard players operation #sec demo.c += #div demo.c
scoreboard players remove #sec demo.c 1
scoreboard players operation #sec demo.c /= #div demo.c
data modify storage demo:arena h set value {lt:"off"}
execute store result storage demo:arena h.sec int 1 run scoreboard players get #sec demo.c
execute store result storage demo:arena h.speed int 1 run scoreboard players get #speed nx.arena
execute if score #lt_on nx.arena matches 1 run data modify storage demo:arena h.lt set value "ON"
function demo:second_m with storage demo:arena h
