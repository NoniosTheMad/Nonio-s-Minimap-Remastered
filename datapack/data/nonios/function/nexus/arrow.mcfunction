# as an arrow within 6 blocks of a Barrier, at the shield (bottom centre of the obsidian). Interaction entities ignore
# projectiles, so arrows are caught by position: within 1 block of the core's centre = a hit (stuck in the obsidian or
# bounced off the shell). Its speed is read every tick before that (nx.arsp = blocks/tick x100), since a stuck arrow has none.
# Damage to the Barrier = 20% of the arrow's (vanilla: speed x base damage, Power adds 0.5/level + 0.5) x10, the
# same x10 scale as melee (nexus/hit). Teammates' and mobs' arrows do nothing and are left alone.
execute positioned ~ ~0.6 ~ unless entity @s[distance=..1] run return run function nonios:nexus/arrow_speed
tag @s add nx.arrow_done
scoreboard players set #ao nx.tmp 0
$execute on owner if entity @s[type=player,team=!$(team)] run scoreboard players set #ao nx.tmp 1
execute if score #ao nx.tmp matches 0 run return 0
execute unless score @s nx.arsp matches 1.. run scoreboard players set @s nx.arsp 300
# base damage x10 (2.0 -> 20) + Power from the bow that shot it
execute store result score #ad nx.tmp run data get entity @s damage 10
execute store result score #pw nx.tmp run data get entity @s weapon.components."minecraft:enchantments"."minecraft:power"
execute if score #pw nx.tmp matches 1.. run scoreboard players operation #pw nx.tmp *= #5 nx.const
execute if score #pw nx.tmp matches 1.. run scoreboard players add #pw nx.tmp 5
scoreboard players operation #ad nx.tmp += #pw nx.tmp
# arsp x ad / 500 = speed x damage x 10 x 20%   (full bow: 300 x 20 / 500 = 12; a sword hit is ~70)
scoreboard players operation #ad nx.tmp *= @s nx.arsp
scoreboard players operation #ad nx.tmp /= #500 nx.const
execute if score #ad nx.tmp matches ..0 run scoreboard players set #ad nx.tmp 1
scoreboard players operation #adm nx.tmp += #ad nx.tmp
execute on owner run scoreboard players operation @s nx.nxdmg += #ad nx.tmp
execute on owner run tag @s add nx.arrow_shooter
kill @s
