# as + at a generator marker after nx.gen_lvl changed: regrow delay + structure.
execute if score @s nx.gen_lvl matches ..0 run scoreboard players set @s nx.gen_lvl 1
execute if score @s nx.gen_lvl matches 4.. run scoreboard players set @s nx.gen_lvl 3
execute store result entity @s data.lvl int 1 run scoreboard players get @s nx.gen_lvl
execute if score @s nx.gen_lvl matches 1 run scoreboard players operation @s nx.gen_iv = #iv1 nx.gen
execute if score @s nx.gen_lvl matches 2 run scoreboard players operation @s nx.gen_iv = #iv2 nx.gen
execute if score @s nx.gen_lvl matches 3 run scoreboard players operation @s nx.gen_iv = #iv3 nx.gen
# a faster level never makes you wait longer than its own delay
scoreboard players operation @s nx.gen_t < @s nx.gen_iv
function nonios:generator/apply_m with entity @s data
particle minecraft:totem_of_undying ~ ~0.8 ~ 0.4 0.4 0.4 0.3 30
playsound minecraft:block.beacon.power_select block @a[distance=..16] ~ ~ ~ 0.8 1.2
