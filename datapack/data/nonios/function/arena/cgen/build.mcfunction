# at the spot on top of the sea lantern: 3x3 bedrock base, sea lantern in a yellow glass ring, then the entities
fill ~-1 ~-2 ~-1 ~1 ~-2 ~1 minecraft:bedrock
fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:yellow_stained_glass
setblock ~ ~-1 ~ minecraft:sea_lantern
setblock ~ ~ ~ minecraft:air
execute align xyz positioned ~0.5 ~ ~0.5 run function nonios:arena/cgen/spawn_at
