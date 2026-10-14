# API: as the player, no class at all (also forgets the basic class, so nothing comes back on respawn)
function nonios:class/strip
scoreboard players set @s nx.cls_basic 0
tellraw @s {"text":"✦ Class removed. You are just you again.","color":"gray"}
