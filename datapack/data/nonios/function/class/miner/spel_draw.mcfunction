# as the ore marker, {c}: a dot just in front of the Miner's eyes, in the ore's direction, so no wall hides it;
# bigger when the ore is within 4 blocks. Only the Miner is sent the particle.
$execute if entity @a[tag=nx.spel_me,distance=..4] at @a[tag=nx.spel_me,limit=1] positioned ~ ~1.5 ~ facing entity @s feet positioned ^ ^ ^0.6 run return run particle minecraft:dust{color:[$(c)],scale:0.6} ~ ~ ~ 0 0 0 0 1 force @a[tag=nx.spel_me]
$execute at @a[tag=nx.spel_me,limit=1] positioned ~ ~1.5 ~ facing entity @s feet positioned ^ ^ ^0.6 run particle minecraft:dust{color:[$(c)],scale:0.35} ~ ~ ~ 0 0 0 0 1 force @a[tag=nx.spel_me]
