# Compatibility for the demos' "generator drop now" button: grow a new block now (only if the spot is empty).
execute if block ~ ~ ~ #minecraft:air run function nonios:generator/grow
