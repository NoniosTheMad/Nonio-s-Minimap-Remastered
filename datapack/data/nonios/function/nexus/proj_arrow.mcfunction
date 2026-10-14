# as an arrow that hit: #ad = speed (|M| x100; 300 if stuck) x (base damage + Power) x10 / 500 = 20% of a player hit, x10
scoreboard players set @s nx.arsp 300
scoreboard players operation #mx nx.tmp = #mm nx.tmp
scoreboard players set #r nx.tmp 200
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run function nonios:nexus/arrow_sqrt
execute if score #mm nx.tmp matches 100.. run scoreboard players operation @s nx.arsp = #r nx.tmp
execute store result score #ad nx.tmp run data get entity @s damage 10
execute store result score #pw nx.tmp run data get entity @s weapon.components."minecraft:enchantments"."minecraft:power"
execute if score #pw nx.tmp matches 1.. run scoreboard players operation #pw nx.tmp *= #5 nx.const
execute if score #pw nx.tmp matches 1.. run scoreboard players add #pw nx.tmp 5
scoreboard players operation #ad nx.tmp += #pw nx.tmp
scoreboard players operation #ad nx.tmp *= @s nx.arsp
scoreboard players operation #ad nx.tmp /= #500 nx.const
