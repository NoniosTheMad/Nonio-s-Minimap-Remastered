# as + at the centre generator: empty pot, full timer, drops around it removed (new match)
scoreboard players set @s nx.gen_pot 0
scoreboard players operation @s nx.gen_t = #cg_iv nx.gen
kill @e[type=item,distance=..3]
function nonios:arena/cgen/scale
function nonios:arena/cgen/holo
