# as + at a generator marker: drop the current block (no loot) and grow one in the current style
tag @s remove nx.gen_one
setblock ~ ~ ~ minecraft:air
function nonios:generator/grow
