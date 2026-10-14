execute store result storage nonios:map area.y int 1 run scoreboard players get #y nx.tmp
scoreboard players add #y nx.tmp 1
execute store result storage nonios:map area.yb int 1 run scoreboard players get #y nx.tmp
function nonios:map/gen/clear_fill with storage nonios:map area
scoreboard players add #y nx.tmp 1
execute if score #y nx.tmp <= #y2 nx.tmp run function nonios:map/gen/clear_step
