# (Re)build every node from storage nonios:arena config.nodes. Safe to run again (old nodes are removed first).
# Node chunks are force-loaded so held nodes keep paying out with nobody nearby.
function nonios:arena/apply_config
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/node/remove with entity @s data
data modify storage nonios:arena tmp.nodes set from storage nonios:arena config.nodes
function nonios:arena/node/setup_next
scoreboard players operation #ev_t nx.arena = #ev_first nx.arena
# random-entry gates + regrowing core (V2)
function nonios:arena/gate/setup
function nonios:arena/core/setup
