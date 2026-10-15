# as + at the core marker: roll and set the block (replaces whatever is there)
tag @s remove nx.c_wait
execute unless score #cwsum nx.arena matches 1.. run return 0
function nonios:arena/core/pick
function nonios:arena/core/set with storage nonios:arena core_pick
