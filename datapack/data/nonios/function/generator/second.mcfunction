# as + at a generator marker, once per second
scoreboard players operation @s nx.gen_t -= #step nx.gen
execute if score @s nx.gen_t matches ..0 run function nonios:generator/drop
function nonios:generator/spin
function nonios:generator/holo
