# as a player leaving the Dream: their pixie goes with them
scoreboard players operation #me nx.dream = @s nx.pid
execute as @e[tag=nx.pixie] if score @s nx.pid = #me nx.dream run kill @s
