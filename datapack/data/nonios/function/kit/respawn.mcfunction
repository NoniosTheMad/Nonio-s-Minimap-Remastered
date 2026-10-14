# Respawn kit hook (STUB). Function tag #nonios:kit/respawn runs as the respawned player (alive, at the team spawn).
# Future: basic-class kit by team upgrade tier (DESIGN §2.8, §6.3); classes add their own function to the tag.
# keep_inventory ON (default): gear is kept, nothing to give. OFF: a minimal kit so nobody respawns empty-handed.
execute if data storage nonios:config {keep_inventory:1b} run return 0
give @s minecraft:stone_sword
give @s minecraft:stone_pickaxe
give @s minecraft:bread 4
