# default #nonios:dream/fallback_return: no remembered spot (e.g. sent in by an admin tp). Teams will hook their spawn here.
# Uses the player's respawn point when they have one, else the surface at overworld 0 0.
execute if data entity @s respawn.pos run return run function nonios:dream/exit/to_respawn
execute in minecraft:overworld run spreadplayers 0 0 0 1 false @s
