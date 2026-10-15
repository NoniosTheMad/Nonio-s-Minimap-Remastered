# Pause the arena: no capture, bonuses, events, lightning, gates, core regrowth or centre generator; bossbars hidden.
# Ownership is kept. An announced event that has not fired yet is dropped.
scoreboard players set #on nx.arena 0
schedule clear nonios:arena/loop
execute as @e[type=marker,tag=nx.node] run function nonios:arena/node/hide with entity @s data
function nonios:arena/bonus/zero
scoreboard players set #ev_wait nx.arena 0
scoreboard players set #ev_run nx.arena 0
bossbar set nonios:arena/event visible false
function nonios:arena/lightning/despawn
function nonios:arena/gate/state
