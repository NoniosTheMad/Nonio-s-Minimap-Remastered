# as + at a generator marker: level 1 and a fresh block (match reset)
scoreboard players set @s nx.gen_lvl 1
function nonios:generator/apply
tag @s remove nx.gen_one
setblock ~ ~ ~ minecraft:air
kill @e[type=item,distance=..2.5]
function nonios:generator/grow
