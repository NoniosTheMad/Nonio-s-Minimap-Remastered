# one Newton step: #r = (#r + #mx / #r) / 2
scoreboard players operation #q nx.tmp = #mx nx.tmp
scoreboard players operation #q nx.tmp /= #r nx.tmp
scoreboard players operation #r nx.tmp += #q nx.tmp
scoreboard players operation #r nx.tmp /= #2 nx.const
execute if score #r nx.tmp matches ..0 run scoreboard players set #r nx.tmp 1
