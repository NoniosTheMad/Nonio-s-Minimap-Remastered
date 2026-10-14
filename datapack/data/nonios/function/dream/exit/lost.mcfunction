# was in the dream, now isn't, and didn't wake up through the channel (died, admin tp...)
tag @s remove nx.in_dream
tag @s remove nx.dream_hold
scoreboard players set @s nx.dch 0
effect clear @s minecraft:jump_boost
data modify storage nonios:dream reason set value "lost"
function #nonios:dream/on_exit
execute store result storage nonios:dream tmp.id int 1 run scoreboard players get @s nx.pid
function nonios:dream/exit/forget with storage nonios:dream tmp
