# walk down (at most 12 blocks) to the first open block standing on something solid
execute if block ~ ~ ~ #demo:mote_air unless block ~ ~-1 ~ #demo:mote_air unless block ~ ~-1 ~ #minecraft:replaceable run return run function demo:angel/emit
scoreboard players add #d demo.st 1
execute if score #d demo.st matches ..12 positioned ~ ~-1 ~ run function demo:angel/scan
