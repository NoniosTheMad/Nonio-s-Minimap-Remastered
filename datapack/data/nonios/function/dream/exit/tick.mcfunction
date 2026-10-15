# as a player in the dream, at them, every tick: the wake-up channel (sneak #channel_ticks; a hit or letting go cancels)
execute if entity @s[tag=nx.dream_hold] unless predicate nonios:dream/sneaking run tag @s remove nx.dream_hold
execute if entity @s[tag=nx.dream_hold] run return 0
execute unless predicate nonios:dream/sneaking run return run function nonios:dream/exit/release
execute if predicate nonios:dream/gliding run return run function nonios:dream/exit/release
execute if score @s nx.dch matches 1.. if score @s nx.dhit matches 1.. run return run function nonios:dream/exit/interrupt
execute if score @s nx.dch matches 1.. if score @s nx.dabs matches 1.. run return run function nonios:dream/exit/interrupt
scoreboard players add @s nx.dch 1
execute if score @s nx.dch >= #channel_ticks nx.dream run return run function nonios:dream/exit/wake
function nonios:dream/exit/progress
