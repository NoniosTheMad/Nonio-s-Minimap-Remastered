# k = 0 .. n-1: curve[k].m
function nonios:bank/curve/idx
scoreboard players operation #c nx.eco = #cn nx.eco
scoreboard players remove #c nx.eco 1
execute if score #ck nx.eco matches 0 run function nonios:bank/curve/tan_first with storage nonios:bank ci
execute if score #ck nx.eco = #c nx.eco run function nonios:bank/curve/tan_last with storage nonios:bank ci
execute if score #ck nx.eco matches 1.. if score #ck nx.eco < #c nx.eco run function nonios:bank/curve/tan_mid with storage nonios:bank ci
scoreboard players add #ck nx.eco 1
execute if score #ck nx.eco < #cn nx.eco run function nonios:bank/curve/tan_loop
