# Gated entry: every function in #nonios:dream/gate runs as the player; any of them can set #deny nx.dream 1
# (and tell the player why) to refuse. Later: team unlock (1000 coins) plugs in here.
scoreboard players set #deny nx.dream 0
function #nonios:dream/gate
execute if score #deny nx.dream matches 1.. run return fail
function nonios:dream/enter
