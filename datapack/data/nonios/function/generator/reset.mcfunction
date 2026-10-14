# as + at a generator marker: level 1, empty pot, full timer
scoreboard players set @s nx.gen_lvl 1
scoreboard players set @s nx.gen_pot 0
function nonios:generator/apply
scoreboard players operation @s nx.gen_t = @s nx.gen_iv
function nonios:generator/holo
