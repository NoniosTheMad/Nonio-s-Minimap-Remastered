# k = 0 .. n-2: curve[k].d = (r[k+1] - r[k]) * 1000 / (t[k+1] - t[k])
function nonios:bank/curve/idx
function nonios:bank/curve/sec with storage nonios:bank ci
scoreboard players add #ck nx.eco 1
scoreboard players operation #c nx.eco = #cn nx.eco
scoreboard players remove #c nx.eco 1
execute if score #ck nx.eco < #c nx.eco run function nonios:bank/curve/sec_loop
