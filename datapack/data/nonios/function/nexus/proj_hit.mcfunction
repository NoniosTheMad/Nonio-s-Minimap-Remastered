# as an enemy projectile that hit the shell. Damage to the Barrier = 20% of what it does to a player, on the x10 melee
# scale (nexus/hit): arrow speed x base damage (+ Power), trident 8, firework rocket 5 + 2 per star, wind charge 1,
# fireball 6, small fireball 5. Added to #adm (nexus/hit_arrow applies the tick's total once).
tag @s add nx.arrow_done
scoreboard players set #ad nx.tmp 0
execute if entity @s[type=#minecraft:arrows] run function nonios:nexus/proj_arrow
execute if entity @s[type=minecraft:trident] run scoreboard players set #ad nx.tmp 16
execute if entity @s[type=minecraft:firework_rocket] run function nonios:nexus/proj_firework
execute if entity @s[type=minecraft:wind_charge] run scoreboard players set #ad nx.tmp 2
execute if entity @s[type=minecraft:fireball] run scoreboard players set #ad nx.tmp 12
execute if entity @s[type=minecraft:small_fireball] run scoreboard players set #ad nx.tmp 10
execute if score #ad nx.tmp matches ..0 run scoreboard players set #ad nx.tmp 1
scoreboard players operation #adm nx.tmp += #ad nx.tmp
execute on owner run scoreboard players operation @s nx.nxdmg += #ad nx.tmp
execute on owner run tag @s add nx.arrow_shooter
execute at @s run particle minecraft:electric_spark ~ ~ ~ 0.15 0.15 0.15 0.2 12
# a trident is the thrower's weapon: it drops at the shell instead (loyalty brings it back)
execute if entity @s[type=minecraft:trident] run return run data modify entity @s Motion set value [0.0d,0.05d,0.0d]
kill @s
