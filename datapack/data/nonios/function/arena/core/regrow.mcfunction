# as + at the core marker: a new block grows in
function nonios:arena/core/place
particle minecraft:happy_villager ~ ~ ~ 0.4 0.4 0.4 0 8
execute if block ~ ~ ~ minecraft:emerald_block run playsound minecraft:block.amethyst_block.chime block @a ~ ~ ~ 1.5 0.8
scoreboard players add #c_grown nx.arena 1
