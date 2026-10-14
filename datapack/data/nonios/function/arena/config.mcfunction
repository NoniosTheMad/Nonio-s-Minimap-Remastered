# ARENA CONFIG: every coordinate and timing of the Arena lives here (storage nonios:arena config).
# Runs on every load, then #nonios:arena/config (a map or demo pack adds a function there to override fields).
# After changing nodes, run `function nonios:arena/setup` to rebuild them. Timings are in game ticks (20 = 1 s).
#
# Capture: every check (10 ticks) a node's progress moves `step` points per capturer (counting up to `max_mult`
# capturers) toward +capture (White) or -capture (Black). Full = captured. Both teams inside = contested (frozen).
# Empty node: progress drifts `decay` per check back to its owner's full value, or toward 0 if unowned.
# Capturers = players of team white/black not in spectator, plus any non-player entity tagged nx.captor on a team.
data modify storage nonios:arena config set value {}
data modify storage nonios:arena config.capture set value 100
data modify storage nonios:arena config.step set value 5
data modify storage nonios:arena config.max_mult set value 3
data modify storage nonios:arena config.decay set value 2
# Payout of a held node, every `payout_every` ticks: first #nonios:arena/on_node_payout runs; if no handler sets
# #handled nx.arena to 1, `loot` drops at the node 1 + (holding team size - 1) / per_roll times (x Golden Hour).
# `coins` (x Golden Hour) is passed to the hook for a team bank. Drops wait while `item_cap` item stacks lie
# within 3 blocks of the node.
data modify storage nonios:arena config.payout_every set value 600
data modify storage nonios:arena config.loot set value "nonios:arena/node"
data modify storage nonios:arena config.coins set value 25
data modify storage nonios:arena config.per_roll set value 4
data modify storage nonios:arena config.item_cap set value 24
# Node indicator: the block at (node centre + indicator_dy) shows the state. A beacon under it = coloured beam.
data modify storage nonios:arena config.indicator set value 1b
data modify storage nonios:arena config.indicator_dy set value -1
data modify storage nonios:arena config.blocks set value {none:"minecraft:yellow_stained_glass",white:"minecraft:white_stained_glass",black:"minecraft:purple_stained_glass",contested:"minecraft:red_stained_glass"}
# Nodes: id (lowercase a-z0-9_, bossbar nonios:arena/<id>), name, x y z = centre block at foot level,
# r = half width (zone = (2r+1) x (2r+1) blocks), h = height in blocks.
# Optional per node: loot (loot table), every (payout ticks), coins.
# PLACEHOLDERS until the real Arena is built.
data modify storage nonios:arena config.nodes set value [{id:"north",name:"North Node",x:0,y:64,z:-24,r:2,h:3},{id:"centre",name:"Centre Node",x:0,y:64,z:0,r:3,h:3},{id:"south",name:"South Node",x:0,y:64,z:24,r:2,h:3}]
# Arena box (x y z = min corner, dx dy dz = size; keeps the Lightning Rabbit in) and centre (rabbit spawn).
data modify storage nonios:arena config.bounds set value {x:-40,y:50,z:-40,dx:80,dy:40,dz:80}
data modify storage nonios:arena config.center set value {x:0,y:65,z:0}
# Timed events: the first `event_first` ticks after start, then every `event_every`; one picked at random by weight.
# Entry: id, name (title), color, sub (subtitle), at (1b = runs at a random node, subtitle ends "at <node>"),
# sound, weight, fn (function; at:1b runs as + at the node marker, at:0b runs as the server).
# Adding an event = one `append` line + its function.
data modify storage nonios:arena config.event_first set value 3600
data modify storage nonios:arena config.event_every set value 6000
data modify storage nonios:arena config.events set value []
data modify storage nonios:arena config.events append value {id:"emerald_surge",name:"EMERALD SURGE",color:"green",sub:"Emeralds are erupting",at:1b,sound:"minecraft:block.beacon.activate",weight:3,fn:"nonios:arena/event/emerald_surge"}
data modify storage nonios:arena config.events append value {id:"frog_rain",name:"IT'S RAINING FROGS",color:"light_purple",sub:"Emerald-stuffed frogs are falling",at:1b,sound:"minecraft:entity.frog.long_jump",weight:2,fn:"nonios:arena/event/frog_rain"}
data modify storage nonios:arena config.events append value {id:"golden_hour",name:"GOLDEN HOUR",color:"gold",sub:"Held nodes pay double for a minute",at:0b,sound:"minecraft:ui.toast.challenge_complete",weight:1,fn:"nonios:arena/event/golden_hour"}
# Event tuning
data modify storage nonios:arena config.surge_waves set value 8
data modify storage nonios:arena config.frogs set value 10
data modify storage nonios:arena config.frog_life set value 1200
data modify storage nonios:arena config.golden_time set value 1200
data modify storage nonios:arena config.golden_mult set value 2
# Lightning (V2 homage): the Lightning Rabbit roams the Arena and calls a bolt on itself every `every` ticks.
# Kill it for its loot; it comes back after `respawn` ticks. `on` = default for a fresh world; at runtime use
# function nonios:arena/lightning/on | off | toggle (remembered across reloads).
data modify storage nonios:arena config.lightning set value {on:0b,every:60,respawn:600}
