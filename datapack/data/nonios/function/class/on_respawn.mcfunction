# HOOK (M2 #nonios:kit/respawn): as/at the respawned player. Re-applies its basic class at the team's current level.
# Call class/on_death first (it removes whatever the player still had).
execute if score @s nx.class matches 1.. run return 0
execute unless score @s nx.cls_basic matches 1.. run return 0
scoreboard players operation @s nx.cls_req = @s nx.cls_basic
function nonios:class/gen/apply
