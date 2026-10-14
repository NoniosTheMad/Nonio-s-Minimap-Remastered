# Pause the arena: no capture, payouts, events, lightning, gates or core regrowth; bossbars hidden. Ownership is kept.
scoreboard players set #on nx.arena 0
schedule clear nonios:arena/loop
execute as @e[type=marker,tag=nx.node] run function nonios:arena/node/hide with entity @s data
function nonios:arena/lightning/despawn
function nonios:arena/gate/state
