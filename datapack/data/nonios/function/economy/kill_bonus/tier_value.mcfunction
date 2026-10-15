# #bonus nx.eco += config tier_bonus[#vtier] (missing index = 0)
execute if score #vtier nx.eco matches ..0 run return 0
execute store result storage nonios:eco tv.i int 1 run scoreboard players get #vtier nx.eco
function nonios:economy/kill_bonus/tier_add with storage nonios:eco tv
