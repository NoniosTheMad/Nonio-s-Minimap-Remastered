# macro {l} (storage mob, set by event/warden), at the guard post
$execute as @e[type=wither_skeleton,tag=nx.ev_warden,limit=1] unless entity @s[distance=..$(l)] at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 15
$execute as @e[type=wither_skeleton,tag=nx.ev_warden,limit=1] unless entity @s[distance=..$(l)] run tp @s ~ ~ ~
