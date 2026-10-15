# Every node back to neutral; payout, event and event-effect timers restarted; event leftovers removed; gates, core and
# centre generator reset.
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/node/reset
function nonios:arena/bonus/zero
scoreboard players operation #ev_t nx.arena = #ev_first nx.arena
scoreboard players set #ev_wait nx.arena 0
scoreboard players set #ev_run nx.arena 0
bossbar set nonios:arena/event visible false
scoreboard players set #mult nx.arena 1
scoreboard players set #golden_t nx.arena 0
scoreboard players set #frog_t nx.arena 0
scoreboard players set #bounty_t nx.arena 0
scoreboard players set #grav_t nx.arena 0
function nonios:arena/event/frogs_despawn
tag @e[type=marker,tag=nx.surge] remove nx.surge
# supply drops: falling or landed chests near the nodes go (contents too)
kill @e[type=falling_block,tag=nx.ev_supply]
execute as @e[type=marker,tag=nx.node] at @s run fill ~-3 ~-2 ~-3 ~3 ~6 ~3 minecraft:air replace minecraft:chest
# gates: fresh active slot; core: fresh block, drops around it removed; centre generator: empty pot
function nonios:arena/gate/reset
function nonios:arena/core/reset
execute as @e[type=marker,tag=nx.cgen] at @s run function nonios:arena/cgen/reset
