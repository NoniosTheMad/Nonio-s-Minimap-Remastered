execute if entity @s[tag=nx.dream_dbg] run return run function demo:say {m:"Site log off",cmd:"tag @s remove nx.dream_dbg"}
scoreboard players set #dbg nx.dream 1
function demo:say {m:"Site log on: new sites are announced to you",cmd:"tag @s add nx.dream_dbg"}
