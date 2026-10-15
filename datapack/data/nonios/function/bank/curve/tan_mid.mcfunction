# harmonic mean 2ab/(a+b) of the secants either side (as (2000a/(a+b)) * b / 1000), 0 when they differ in sign
$execute store result score #a nx.eco run data get storage nonios:bank curve[$(k0)].d
$execute store result score #b nx.eco run data get storage nonios:bank curve[$(k)].d
scoreboard players set #m nx.eco 0
execute if score #a nx.eco matches 1.. if score #b nx.eco matches 1.. run function nonios:bank/curve/hmean
execute if score #a nx.eco matches ..-1 if score #b nx.eco matches ..-1 run function nonios:bank/curve/hmean
$execute store result storage nonios:bank curve[$(k)].m int 1 run scoreboard players get #m nx.eco
