# Create a generator. Run positioned at the block on top of the sea lantern; macro {team:"white"|"black", lvl:1..3}.
# The level structure (3x3x2: bedrock base, sea lantern, glass) is placed with its base two blocks below.
$execute align xyz positioned ~0.5 ~ ~0.5 run function nonios:generator/spawn_at {team:"$(team)",lvl:$(lvl)}
