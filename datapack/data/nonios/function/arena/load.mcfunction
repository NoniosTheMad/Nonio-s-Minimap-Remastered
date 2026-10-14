# Arena (DESIGN 2.10): contested nodes, timed events, lightning. One schedule loop every 10 ticks; nothing per tick.
#
# API
#   function nonios:arena/setup            (re)build the nodes from storage nonios:arena config (markers, bossbars, holograms)
#   function nonios:arena/start | stop     run / pause the arena loop (stop hides bossbars; ownership is kept)
#   function nonios:arena/reset            every node back to neutral, timers restarted, event leftovers removed
#   function nonios:arena/event/random     fire a random event now;  event/start {i:N} fires config.events[N]
#   function nonios:arena/lightning/on | off | toggle
#   function nonios:arena/status           prints every node (owner, progress, next payout) to @s
# Hooks (function tags)
#   #nonios:arena/config          runs after the default config on every load: override storage fields there
#   #nonios:arena/on_node_payout  as + at the node marker; storage nonios:arena payout = {team,node,name,loot,rolls,coins}.
#                                 A handler that pays the team itself sets #handled nx.arena 1, else the loot drops.
#   #nonios:arena/on_capture      as + at the node marker; storage nonios:arena cap = {team,node,name}; team "" = neutralised
# Scores on a node marker: nx.ar_cap (-capture..capture, + = White), nx.ar_own (0 none, 1 white, 2 black),
# nx.ar_t (ticks to next payout), nx.ar_iv (payout interval), nx.ar_st (display code).
# Globals in nx.arena: #on, #speed (timer multiplier), #mult (payout multiplier), #ev_t (ticks to next event).
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.arena dummy
scoreboard objectives add nx.ar_cap dummy
scoreboard objectives add nx.ar_own dummy
scoreboard objectives add nx.ar_t dummy
scoreboard objectives add nx.ar_iv dummy
scoreboard objectives add nx.ar_st dummy
scoreboard objectives add nx.ar_ev dummy
scoreboard players set #0 nx.arena 0
scoreboard players set #-1 nx.arena -1
scoreboard players set #10 nx.arena 10
scoreboard players set #20 nx.arena 20
scoreboard players set #100 nx.arena 100
execute unless score #speed nx.arena matches 1.. run scoreboard players set #speed nx.arena 1
execute unless score #mult nx.arena matches 1.. run scoreboard players set #mult nx.arena 1
function nonios:arena/config
function #nonios:arena/config
function nonios:arena/apply_config
execute if score #on nx.arena matches 1 run schedule function nonios:arena/loop 10t replace
