# actionbar bar (30 segments) + seconds left; rising chime every 5 ticks that everyone nearby hears
scoreboard players operation #n nx.dream = @s nx.dch
scoreboard players operation #n nx.dream *= #30 nx.dream
scoreboard players operation #n nx.dream /= #channel_ticks nx.dream
execute store result storage nonios:dream bar.n int 1 run scoreboard players get #n nx.dream
scoreboard players operation #s nx.dream = #channel_ticks nx.dream
scoreboard players operation #s nx.dream -= @s nx.dch
scoreboard players add #s nx.dream 19
scoreboard players operation #s nx.dream /= #20 nx.dream
execute store result storage nonios:dream bar.s int 1 run scoreboard players get #s nx.dream
function nonios:dream/exit/bar with storage nonios:dream bar
scoreboard players operation #t5 nx.dream = @s nx.dch
scoreboard players operation #t5 nx.dream %= #5 nx.dream
execute unless score #t5 nx.dream matches 0 run return 0
scoreboard players operation #p nx.dream = @s nx.dch
scoreboard players operation #p nx.dream *= #150 nx.dream
scoreboard players operation #p nx.dream /= #channel_ticks nx.dream
scoreboard players add #p nx.dream 50
execute store result storage nonios:dream bar.p float 0.01 run scoreboard players get #p nx.dream
function nonios:dream/exit/chime with storage nonios:dream bar
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.8 0.5 0 3
particle minecraft:end_rod ~ ~0.2 ~ 0.6 0 0.6 0.02 2
