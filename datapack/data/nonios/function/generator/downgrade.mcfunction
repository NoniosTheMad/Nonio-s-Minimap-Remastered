# as + at a generator marker. Fails (returns 0) at level 1.
execute if score @s nx.gen_lvl matches ..1 run return fail
scoreboard players remove @s nx.gen_lvl 1
function nonios:generator/apply
return 1
