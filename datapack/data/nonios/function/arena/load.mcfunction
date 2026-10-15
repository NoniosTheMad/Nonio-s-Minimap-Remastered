# Arena (DESIGN 2.10): capture nodes (team bonuses), announced events, centre generator, lightning, gates, core,
# protection of the arena's own blocks. One schedule loop every 10 ticks; per tick only gate/tick + protect/tick.
#
# API
#   function nonios:arena/setup            (re)build nodes, gates, core, centre generator and the protection backup
#   function nonios:arena/start | stop     run / pause the arena loop (stop hides bossbars; ownership is kept)
#   function nonios:arena/reset            every node back to neutral, timers restarted, event leftovers removed
#   function nonios:arena/event/random     announce a random event now (it fires event_warn ticks later)
#   function nonios:arena/event/start {i:N}   announce config.events[N];  event/now {i:N}: fire it at once
#   function nonios:arena/lightning/on | off | toggle
#   function nonios:arena/status           prints nodes, bonuses, events, gates, core, centre generator to @s
#   function nonios:arena/gate/rotate      re-roll the active gate slot now;  gate/status, core/status, cgen/status
#   function nonios:arena/core/regrow      (as + at the nx.acore marker) roll a new core block now
# Nodes (feedback #40) are a sub-objective: holding one gives its team a small bonus (config.nodes[].bonus):
#   haste    Haste I for the team inside its own field (config.fields.<team>)
#   interest every payout_every ticks the team bank gains interest_permille of itself (max interest_cap) x #mult
#   regrow   the team's field generator regrows 50% faster (generator/loop reads #regrow_<team> nx.arena)
#   Counters #<bonus>_<team> nx.arena = held nodes with that bonus, recounted every loop. A node only drops loot
#   if it has an explicit `loot`.
# Events (feedback #42): announced event_warn ticks ahead with bossbar nonios:arena/event (countdown + raid horn);
#   timed events then show their remaining time on the same bar. Troll events (troll:1b) only with config.trolls.
# Centre generator (arena/cgen): shared pot-style generator at config.cgen; stronger the more coins both banks hold.
# Protection (arena/protect, feedback #43): config.protect = the arena's own blocks; a backup copy below restores
#   any of them every tick (players can still build in the air); their drops vanish, their coins are cancelled.
# Gates (V2 random-entry portals): markers nx.agate (+ nx.<team>) on the pads, nx.aslot at each slot exit (nx.ar_slot = 1..),
#   nx.aslot_on = the active one. #gon = open (arena on + gates + slots), #slot / #slots, #g_t = ticks to the next roll.
# Core (V2 regrowing block): marker nx.acore in the block, #core = 1 if set.
# Hooks (function tags)
#   #nonios:arena/config          runs after the default config on every load: override storage fields there
#   #nonios:arena/on_node_payout  as + at the node marker; storage nonios:arena payout = {team,node,name,loot,rolls,coins}.
#                                 A handler that pays the team itself sets #handled nx.arena 1, else the loot (if any) drops.
#   #nonios:arena/on_capture      as + at the node marker; storage nonios:arena cap = {team,node,name}; team "" = neutralised
# Scores on a node marker: nx.ar_cap (-capture..capture, + = White), nx.ar_own (0 none, 1 white, 2 black),
# nx.ar_t (ticks to next payout), nx.ar_iv (payout interval), nx.ar_st (display code).
# Globals in nx.arena: #on, #speed (timer multiplier), #mult (payout multiplier), #ev_t (ticks to next event),
# #ev_wait (announced event: ticks until it fires), #ev_run (running event: ticks left).
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.arena dummy
scoreboard objectives add nx.ar_cap dummy
scoreboard objectives add nx.ar_own dummy
scoreboard objectives add nx.ar_t dummy
scoreboard objectives add nx.ar_iv dummy
scoreboard objectives add nx.ar_st dummy
scoreboard objectives add nx.ar_ev dummy
scoreboard objectives add nx.ar_slot dummy
# centre generator scores (shared with generator/): level, timer, pot, pot cap
scoreboard objectives add nx.gen dummy
scoreboard objectives add nx.gen_lvl dummy
scoreboard objectives add nx.gen_t dummy
scoreboard objectives add nx.gen_pot dummy
scoreboard objectives add nx.gen_cap dummy
scoreboard objectives add nx.bank dummy
scoreboard players set #0 nx.arena 0
scoreboard players set #-1 nx.arena -1
scoreboard players set #10 nx.arena 10
scoreboard players set #20 nx.arena 20
scoreboard players set #100 nx.arena 100
scoreboard players set #1000 nx.arena 1000
execute unless score #speed nx.arena matches 1.. run scoreboard players set #speed nx.arena 1
execute unless score #mult nx.arena matches 1.. run scoreboard players set #mult nx.arena 1
bossbar add nonios:arena/event ""
bossbar set nonios:arena/event style notched_10
function nonios:arena/cgen/config
function nonios:arena/config
function #nonios:arena/config
function nonios:arena/apply_config
execute if score #on nx.arena matches 1 run schedule function nonios:arena/loop 10t replace
