# advancement nonios:game/dummy_killed (a player killed a test dummy): counts as a kill, may end the match
advancement revoke @s only nonios:game/dummy_killed
scoreboard players add @s nx.kills 1
function nonios:game/win_check
