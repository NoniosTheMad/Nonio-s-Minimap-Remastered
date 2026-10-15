# #ct nx.eco = match seconds -> #ppm nx.eco = the curve there (flat before the first and after the last point)
scoreboard players set #ppm nx.eco 0
execute if score #cn nx.eco matches ..0 run return 0
execute store result score #ppm nx.eco run data get storage nonios:bank curve[0].r
execute if score #cn nx.eco matches 1 run return 0
execute store result score #a nx.eco run data get storage nonios:bank curve[0].t
execute if score #ct nx.eco <= #a nx.eco run return 0
execute store result score #ppm nx.eco run data get storage nonios:bank curve[-1].r
execute store result score #a nx.eco run data get storage nonios:bank curve[-1].t
execute if score #ct nx.eco >= #a nx.eco run return 0
# segment k: the last point with t <= #ct
scoreboard players set #ck nx.eco 0
function nonios:bank/curve/find
function nonios:bank/curve/idx
function nonios:bank/curve/herm with storage nonios:bank ci
