# as a player: match reset (game/enter for a new match, lobby_player): no class at all, nothing comes back on respawn. Silent.
function nonios:class/strip
scoreboard players set @s nx.cls_basic 0
scoreboard players set @s nx.cls_askst 0
