# as a node while the arena runs: shown = from + (target - from) x min(#ph, 10) / 10, bossbar = |shown|
scoreboard players operation #k nx.arena = #ph nx.arena
scoreboard players operation #k nx.arena < #10 nx.arena
scoreboard players operation #v nx.arena = #tgt nx.arena
scoreboard players operation #v nx.arena -= @s nx.ar_from
scoreboard players operation #v nx.arena *= #k nx.arena
scoreboard players operation #v nx.arena /= #10 nx.arena
scoreboard players operation #v nx.arena += @s nx.ar_from
execute if score @s nx.ar_shw = #v nx.arena run return 0
scoreboard players operation @s nx.ar_shw = #v nx.arena
scoreboard players operation #abs nx.arena = #v nx.arena
execute if score #abs nx.arena matches ..-1 run scoreboard players operation #abs nx.arena *= #-1 nx.arena
function nonios:arena/node/bar with entity @s data
