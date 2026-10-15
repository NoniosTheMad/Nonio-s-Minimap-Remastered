# as + at the centre generator: its level changed to #cl
execute if score @s nx.gen_lvl matches 1.. if score #cl nx.arena > @s nx.gen_lvl run function nonios:arena/cgen/level_up
scoreboard players operation @s nx.gen_lvl = #cl nx.arena
execute if score #cl nx.arena matches 1 run scoreboard players operation @s nx.gen_cap = #cg_cap1 nx.gen
execute if score #cl nx.arena matches 2 run scoreboard players operation @s nx.gen_cap = #cg_cap2 nx.gen
execute if score #cl nx.arena matches 3 run scoreboard players operation @s nx.gen_cap = #cg_cap3 nx.gen
scoreboard players operation @s nx.gen_pot < @s nx.gen_cap
execute store result storage nonios:arena cg.lvl int 1 run scoreboard players get #cl nx.arena
function nonios:arena/cgen/level_m with storage nonios:arena cg
