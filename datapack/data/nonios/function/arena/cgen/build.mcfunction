# at the spot on top of the core block: 3x3 bedrock base, emerald block in a lime glass ring, then the entities
fill ~-1 ~-2 ~-1 ~1 ~-2 ~1 minecraft:bedrock
fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:lime_stained_glass
setblock ~ ~-1 ~ minecraft:emerald_block
setblock ~ ~ ~ minecraft:air
execute align xyz positioned ~0.5 ~ ~0.5 run function nonios:arena/cgen/spawn_at
