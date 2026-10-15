function nonios:bank/curve/idx
function nonios:bank/curve/next_t with storage nonios:bank ci
execute if score #ct nx.eco >= #a nx.eco run scoreboard players add #ck nx.eco 1
execute if score #ct nx.eco >= #a nx.eco run function nonios:bank/curve/find
