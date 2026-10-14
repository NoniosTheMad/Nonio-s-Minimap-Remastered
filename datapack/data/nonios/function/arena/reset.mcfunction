# Every node back to neutral; payout, event and Golden Hour timers restarted; event leftovers removed.
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/node/reset
scoreboard players operation #ev_t nx.arena = #ev_first nx.arena
scoreboard players set #mult nx.arena 1
scoreboard players set #golden_t nx.arena 0
scoreboard players set #frog_t nx.arena 0
function nonios:arena/event/frogs_despawn
tag @e[type=marker,tag=nx.surge] remove nx.surge
