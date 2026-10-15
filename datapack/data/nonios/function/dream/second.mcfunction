# once a second, positioned in the Dream
function nonios:dream/site/second
function nonios:dream/fauna/tick
function nonios:dream/nightmare/tick
execute as @e[tag=nx.pixie,distance=0..] at @s run function nonios:dream/pixie/gc
# endermen are not part of the dream (user #81); old ones from v2 drift away into the void
tp @e[type=minecraft:enderman,distance=0..] ~ -200 ~
