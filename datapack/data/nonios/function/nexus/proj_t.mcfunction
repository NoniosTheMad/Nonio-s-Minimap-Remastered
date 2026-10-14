# #t = clamp(D.M * 1000 / M.M, 0, 1000)
scoreboard players operation #t nx.tmp = #dx nx.tmp
scoreboard players operation #t nx.tmp *= #mx nx.tmp
scoreboard players operation #q nx.tmp = #dy nx.tmp
scoreboard players operation #q nx.tmp *= #my nx.tmp
scoreboard players operation #t nx.tmp += #q nx.tmp
scoreboard players operation #q nx.tmp = #dz nx.tmp
scoreboard players operation #q nx.tmp *= #mz nx.tmp
scoreboard players operation #t nx.tmp += #q nx.tmp
execute if score #t nx.tmp matches ..0 run return run scoreboard players set #t nx.tmp 0
scoreboard players operation #t nx.tmp *= #1000 nx.const
scoreboard players operation #t nx.tmp /= #mm nx.tmp
execute if score #t nx.tmp matches 1001.. run scoreboard players set #t nx.tmp 1000
