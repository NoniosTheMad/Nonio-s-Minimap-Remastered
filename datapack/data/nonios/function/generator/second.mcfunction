# as + at a generator marker, once per second
# the sea lantern / base went missing (explosion, creative): put the level structure back
execute unless block ~ ~-1 ~ minecraft:sea_lantern run function nonios:generator/apply_m with entity @s data
# something is on the spot: the regrow timer waits (it starts when the block is mined)
execute unless block ~ ~ ~ #minecraft:air run return run scoreboard players operation @s nx.gen_t = @s nx.gen_iv
execute if entity @s[tag=nx.gen.white] run scoreboard players operation @s nx.gen_t -= #st_white nx.gen
execute if entity @s[tag=nx.gen.black] run scoreboard players operation @s nx.gen_t -= #st_black nx.gen
particle minecraft:end_rod ~ ~0.3 ~ 0.15 0.05 0.15 0.01 1
execute if score @s nx.gen_t matches ..0 run function nonios:generator/grow
