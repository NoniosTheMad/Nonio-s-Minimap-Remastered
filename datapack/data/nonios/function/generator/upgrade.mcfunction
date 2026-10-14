# as + at a generator marker. Fails (returns 0) at max level.
execute if score @s nx.gen_lvl matches 3.. run return fail
scoreboard players add @s nx.gen_lvl 1
function nonios:generator/apply
return 1
