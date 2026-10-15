# Wake @s up immediately (no channel). Admin/demo/game-end use.
execute at @s unless dimension nonios:emerald_dream unless entity @s[tag=nx.dream_arriving] run return fail
tag @s remove nx.dream_arriving
data modify storage nonios:dream reason set value "forced"
function nonios:dream/exit/send
