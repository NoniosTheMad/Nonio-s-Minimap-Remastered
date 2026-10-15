# #ck nx.eco -> storage nonios:bank ci {k, k1 = k+1, k0 = k-1}
execute store result storage nonios:bank ci.k int 1 run scoreboard players get #ck nx.eco
execute store result storage nonios:bank ci.k1 int 1 run scoreboard players add #ck nx.eco 1
execute store result storage nonios:bank ci.k0 int 1 run scoreboard players remove #ck nx.eco 2
scoreboard players add #ck nx.eco 1
