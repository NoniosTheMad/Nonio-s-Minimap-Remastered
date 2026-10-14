# as/at the Barrier of $(team), past battle minute #decay_min: its ceiling (nx.hp_cap) drops max x #decay_pm per mille
# per minute; HP above the ceiling goes with it and regen stops at it. Ceiling 0 = Barrier down.
scoreboard players operation #q nx.tmp = @s nx.hp_max
scoreboard players operation #q nx.tmp *= #decay_pm nx.const
scoreboard players operation @s nx.dca += #q nx.tmp
scoreboard players operation #d nx.tmp = @s nx.dca
scoreboard players operation #d nx.tmp /= #60000 nx.const
execute if score #d nx.tmp matches ..0 run return 0
scoreboard players operation #q nx.tmp = #d nx.tmp
scoreboard players operation #q nx.tmp *= #60000 nx.const
scoreboard players operation @s nx.dca -= #q nx.tmp
scoreboard players operation @s nx.hp_cap -= #d nx.tmp
execute if score @s nx.hp > @s nx.hp_cap run scoreboard players operation @s nx.hp = @s nx.hp_cap
execute if score @s nx.hp_cap matches ..0 run scoreboard players set @s nx.hp 0
particle minecraft:falling_obsidian_tear ~ ~1.1 ~ 0.4 0.1 0.4 0 1
$execute if score @s nx.hp matches ..0 run function nonios:nexus/broken {team:"$(team)"}
