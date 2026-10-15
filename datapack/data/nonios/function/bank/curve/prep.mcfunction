# nonios:bank curve (a copy of a config curve) -> #cn points, each with d (secant) and m (tangent); see bank/curve/build
execute store result score #cn nx.eco run data get storage nonios:bank curve
execute if score #cn nx.eco matches ..1 run return 0
scoreboard players set #ck nx.eco 0
function nonios:bank/curve/sec_loop
scoreboard players set #ck nx.eco 0
function nonios:bank/curve/tan_loop
