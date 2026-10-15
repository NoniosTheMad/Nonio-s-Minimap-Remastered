# as/at the Angel, beam up but no ally found: a thin stream of light along the aim, every 4th tick
execute store result score #p nx.cls_tmp run time query gametime
scoreboard players operation #p nx.cls_tmp %= #4 nx.cls_tmp
execute unless score #p nx.cls_tmp matches 0 run return 0
execute anchored eyes positioned ^-0.35 ^-0.3 ^0.7 run particle minecraft:end_rod ~ ~ ~ 0.02 0.02 0.02 0.005 1 normal
