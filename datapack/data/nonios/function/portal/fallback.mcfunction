# #nonios:dream/fallback_return (as the player, no valid way back): team spawn during a match, else the lobby.
# Without the match map (dream demo): the dream's default (respawn point).
execute unless score #map nx.state matches 1 run return run function nonios:dream/exit/fallback_default
execute if score #state nx.state matches 1..3 if entity @s[team=white] run return run function nonios:game/tp_spawn with storage nonios:map white.spawn
execute if score #state nx.state matches 1..3 if entity @s[team=black] run return run function nonios:game/tp_spawn with storage nonios:map black.spawn
function nonios:game/tp_lobby with storage nonios:map lobby
