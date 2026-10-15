# #fit = lots of sel that fit in the empty main-inventory slots: empty x stack / count (count = one lot)
scoreboard players set #free nx.tmp 0
execute unless items entity @s container.0 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.1 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.2 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.3 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.4 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.5 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.6 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.7 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.8 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.9 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.10 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.11 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.12 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.13 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.14 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.15 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.16 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.17 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.18 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.19 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.20 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.21 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.22 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.23 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.24 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.25 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.26 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.27 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.28 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.29 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.30 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.31 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.32 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.33 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.34 * run scoreboard players add #free nx.tmp 1
execute unless items entity @s container.35 * run scoreboard players add #free nx.tmp 1
execute store result score #fit nx.tmp run data get storage nonios:shop sel.stack
execute if score #fit nx.tmp matches ..0 run scoreboard players set #fit nx.tmp 64
scoreboard players operation #fit nx.tmp *= #free nx.tmp
execute store result score #q nx.tmp run data get storage nonios:shop sel.base
execute if score #q nx.tmp matches ..0 run scoreboard players set #q nx.tmp 1
scoreboard players operation #fit nx.tmp /= #q nx.tmp
