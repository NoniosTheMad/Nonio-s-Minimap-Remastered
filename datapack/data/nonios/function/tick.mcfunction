# One tick for the whole game pack. Each subsystem is cheap when idle (selectors on tags/scores, no bare @e scans).
# game/tick branches on #state nx.state (0 lobby, 1 prep, 2 battle, 3 end) and only runs the current phase.
function nonios:game/tick
function nonios:nexus/tick
function nonios:shop/tick
function nonios:arena/protect/tick
function nonios:purse/tick
function nonios:economy/tick
function nonios:dream/tick
function nonios:generator/tick
function nonios:portal/tick
function nonios:class/tick
function nonios:arena/gate/tick
function nonios:arena/event/tick
function nonios:guard/tick
# deaths: handled once the player has respawned (@e skips dead players), so kits/gamemode apply to the new body
execute as @e[type=player,scores={nx.died=1..}] at @s run function nonios:death
