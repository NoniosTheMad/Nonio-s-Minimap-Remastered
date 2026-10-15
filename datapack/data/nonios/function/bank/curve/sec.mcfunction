$execute store result score #a nx.eco run data get storage nonios:bank curve[$(k1)].r
$execute store result score #b nx.eco run data get storage nonios:bank curve[$(k)].r
scoreboard players operation #a nx.eco -= #b nx.eco
scoreboard players operation #a nx.eco *= #1000 nx.eco
$execute store result score #h nx.eco run data get storage nonios:bank curve[$(k1)].t
$execute store result score #b nx.eco run data get storage nonios:bank curve[$(k)].t
scoreboard players operation #h nx.eco -= #b nx.eco
execute if score #h nx.eco matches ..0 run scoreboard players set #h nx.eco 1
scoreboard players operation #a nx.eco /= #h nx.eco
$execute store result storage nonios:bank curve[$(k)].d int 1 run scoreboard players get #a nx.eco
