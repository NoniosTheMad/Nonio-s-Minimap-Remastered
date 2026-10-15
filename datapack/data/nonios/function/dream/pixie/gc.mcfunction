# once a second, as each pixie part: gone when its dreamer isn't within reach in the Dream (woke, died, logged out)
scoreboard players operation #o nx.dream = @s nx.pid
scoreboard players set #ok nx.dream 0
execute as @a[tag=nx.in_dream,tag=!nx.dream_arriving,distance=..8] if score @s nx.pid = #o nx.dream run scoreboard players set #ok nx.dream 1
execute if score #ok nx.dream matches 0 run kill @s
