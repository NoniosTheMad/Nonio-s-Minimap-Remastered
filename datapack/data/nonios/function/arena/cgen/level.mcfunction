# as + at the centre generator: its level changed to #cl
execute if score @s nx.gen_lvl matches 1.. if score #cl nx.arena > @s nx.gen_lvl run function nonios:arena/cgen/level_up
scoreboard players operation @s nx.gen_lvl = #cl nx.arena
execute store result storage nonios:arena cg.lvl int 1 run scoreboard players get #cl nx.arena
function nonios:arena/cgen/level_m with storage nonios:arena cg
