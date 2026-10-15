# exactly the blocks my team's next altar step still needs (nothing once the altar is fulfilled)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
function nonios:altar/max
scoreboard players operation #lvl nx.altar = #white nx.cls_lvl
execute if entity @s[team=black] run scoreboard players operation #lvl nx.altar = #black nx.cls_lvl
execute if score #lvl nx.altar >= #max nx.altar run return run tellraw @s {"text":"[demo] Your altar is already fulfilled (top level).","color":"yellow"}
execute store result storage nonios:altar arg.i int 1 run scoreboard players get #lvl nx.altar
function nonios:altar/need with storage nonios:altar arg
execute store result storage demo:tmp off.i int 1 run scoreboard players get #ni nx.altar
execute store result storage demo:tmp off.g int 1 run scoreboard players get #ng nx.altar
execute store result storage demo:tmp off.d int 1 run scoreboard players get #nd nx.altar
function demo:offering_give with storage demo:tmp off
