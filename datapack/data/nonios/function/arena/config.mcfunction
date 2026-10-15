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
# Node bonus (feedback #40, #127: nodes give only their bonus, never items). Per node `bonus`: none | haste | interest |
# regrow, and two spare ones no node uses by default: swift | ward (see arena/load). bonus_text = what the bossbar says.
data modify storage nonios:arena config.bonus set value "none"
data modify storage nonios:arena config.bonus_text set value {none:"",haste:"Haste in your field",interest:"Bank +0.5%",regrow:"Generator regrows faster",swift:"Speed in the Arena",ward:"Resistance in the Arena"}
data modify storage nonios:arena config.interest_permille set value 5
data modify storage nonios:arena config.interest_cap set value 10
# Team fields for the haste bonus: {white:{team,x,y,z,dx,dy,dz}, black:{...}} (a map fills them).
data modify storage nonios:arena config.fields set value {}
# Payout of a held node, every `payout_every` ticks: #nonios:arena/on_node_payout runs and the interest bonus pays.
data modify storage nonios:arena config.payout_every set value 600
# Runes (feedback #126): every node shows an Elder Futhark rune in particles over its zone (its identity; no hologram,
# no beacon). config.runes + config.rune_of (bonus -> rune) come from src/runes.json (tools/build_runes.py); a node's
# own `rune` field overrides. Colours = particle specs: neutral / white / black / contested, `cold` = not yet painted.
#   every = ticks between redraws (idle; `every_cap` while it is being captured), view = draw distance (blocks),
#   lift = glyph centre above the zone top, in tenths of a block. ring = the zone outline on the ground.
function nonios:arena/rune/gen/defs
data modify storage nonios:arena config.rune set value {every:3,every_cap:2,view:48,lift:20}
data modify storage nonios:arena config.rune.col set value {neutral:"minecraft:dust{color:[1.0,0.72,0.2],scale:1.6}",white:"minecraft:dust{color:[1.0,1.0,1.0],scale:1.8}",black:"minecraft:dust{color:[0.68,0.3,1.0],scale:1.8}",white_pulse:"minecraft:dust{color:[1.0,1.0,1.0],scale:2.4}",black_pulse:"minecraft:dust{color:[0.68,0.3,1.0],scale:2.4}",cold:"minecraft:dust{color:[0.75,0.55,0.25],scale:1.0}",contested:"minecraft:dust{color:[1.0,0.15,0.1],scale:1.2}",tip:"minecraft:end_rod"}
data modify storage nonios:arena config.rune.ring set value {neutral:"minecraft:dust{color:[1.0,0.72,0.2],scale:0.7}",white:"minecraft:dust{color:[1.0,1.0,1.0],scale:0.7}",black:"minecraft:dust{color:[0.68,0.3,1.0],scale:0.7}",contested:"minecraft:dust{color:[1.0,0.15,0.1],scale:0.8}"}
# Nodes: id (lowercase a-z0-9_, bossbar nonios:arena/<id>), name (status/admin only), x y z = centre block at foot level,
# r = half width (zone = (2r+1) x (2r+1) blocks), h = height in blocks.
# Optional per node: bonus, rune (else config.rune_of.<bonus>), every (payout ticks).
# PLACEHOLDERS until the real Arena is built.
data modify storage nonios:arena config.nodes set value [{id:"north",name:"North Node",x:0,y:64,z:-24,r:2,h:3,bonus:"haste"},{id:"centre",name:"Centre Node",x:0,y:64,z:0,r:3,h:3,bonus:"interest"},{id:"south",name:"South Node",x:0,y:64,z:24,r:2,h:3,bonus:"regrow"}]
# Arena box (x y z = min corner, dx dy dz = size; keeps the Lightning Rabbit in, bounds the bounty / low gravity
# events) and centre (rabbit spawn).
data modify storage nonios:arena config.bounds set value {x:-40,y:50,z:-40,dx:80,dy:40,dz:80}
data modify storage nonios:arena config.center set value {x:0,y:65,z:0}
# Events: the first is announced `event_first` ticks after start, then one every `event_every`; picked at random by
# weight. Each is announced `event_warn` ticks ahead (bossbar countdown + raid horn), then fires.
# Entry: id, name (title), color (text), bar (bossbar colour), sub (subtitle), at (1b = at a random node), sound,
# weight, fn (at:1b runs as + at the node marker, at:0b as the server), troll (1b = only when config.trolls is 1b).
# A timed event's fn sets #ev_run nx.arena to its duration (the bossbar then counts it down).
data modify storage nonios:arena config.event_first set value 3600
data modify storage nonios:arena config.event_every set value 6000
data modify storage nonios:arena config.event_warn set value 600
data modify storage nonios:arena config.trolls set value 0b
data modify storage nonios:arena config.events set value []
data modify storage nonios:arena config.events append value {id:"emerald_surge",name:"EMERALD SURGE",color:"green",bar:"green",sub:"Emeralds erupt",at:1b,sound:"minecraft:block.beacon.activate",weight:3,fn:"nonios:arena/event/emerald_surge"}
data modify storage nonios:arena config.events append value {id:"supply_drop",name:"SUPPLY DROP",color:"aqua",bar:"blue",sub:"A supply chest falls",at:1b,sound:"minecraft:item.trident.thunder",weight:3,fn:"nonios:arena/event/supply_drop"}
data modify storage nonios:arena config.events append value {id:"golden_hour",name:"GOLDEN HOUR",color:"gold",bar:"yellow",sub:"Arena coins x2",at:0b,sound:"minecraft:ui.toast.challenge_complete",weight:2,fn:"nonios:arena/event/golden_hour"}
data modify storage nonios:arena config.events append value {id:"bounty_hunt",name:"BOUNTY HUNT",color:"red",bar:"red",sub:"Kills in the Arena pay extra",at:0b,sound:"minecraft:entity.evoker.prepare_attack",weight:2,fn:"nonios:arena/event/bounty_hunt"}
data modify storage nonios:arena config.events append value {id:"frog_rain",name:"IT'S RAINING FROGS",color:"light_purple",bar:"pink",sub:"Emerald-stuffed frogs fall",at:1b,sound:"minecraft:entity.frog.long_jump",weight:1,troll:1b,fn:"nonios:arena/event/frog_rain"}
data modify storage nonios:arena config.events append value {id:"warband",name:"WARBAND",color:"dark_red",bar:"red",sub:"Raiders storm the Arena",at:0b,sound:"minecraft:event.raid.horn",weight:2,fn:"nonios:arena/event/warband"}
data modify storage nonios:arena config.events append value {id:"warden",name:"THE GILDED WARDEN",color:"gold",bar:"yellow",sub:"A guardian rises by the generator",at:0b,sound:"minecraft:entity.wither_skeleton.ambient",weight:2,fn:"nonios:arena/event/warden"}
data modify storage nonios:arena config.events append value {id:"graves",name:"GRAVES OPEN",color:"dark_green",bar:"green",sub:"The dead rise at every node",at:0b,sound:"minecraft:entity.zombie.ambient",weight:2,fn:"nonios:arena/event/graves"}
# Event tuning
data modify storage nonios:arena config.surge_waves set value 8
data modify storage nonios:arena config.supply_height set value 24
data modify storage nonios:arena config.golden_time set value 1200
data modify storage nonios:arena config.golden_mult set value 2
data modify storage nonios:arena config.bounty_time set value 1200
data modify storage nonios:arena config.bounty_coins set value 50
data modify storage nonios:arena config.gravity_time set value 900
data modify storage nonios:arena config.frogs set value 10
data modify storage nonios:arena config.frog_life set value 1200
# Enemy events (emerald drops only; event mobs are leashed to config.bounds and vanish on stop/reset):
# warband: `waves` waves of `size` raiders every `gap` ticks within `range` of config.center, survivors leave after `life`.
# warden: one boss with `hp` at the centre generator, never more than `leash` blocks from it, withdraws after `life`.
# graves: `per_node` husks (one Grave Lord) at every node, leftovers crumble after `life`.
data modify storage nonios:arena config.warband set value {waves:3,size:4,gap:300,life:1800,range:12}
data modify storage nonios:arena config.warden set value {hp:120,life:2400,leash:10}
data modify storage nonios:arena config.graves set value {per_node:3,life:1200}
# Lightning (V2 homage): the Lightning Rabbit roams the Arena and calls a bolt on itself every `every` ticks.
# Kill it for its loot; it comes back after `respawn` ticks. `on` = default for a fresh world; at runtime use
# function nonios:arena/lightning/on | off | toggle (remembered across reloads).
data modify storage nonios:arena config.lightning set value {on:0b,every:60,respawn:600}
# Random-entry gates (V2 arena portals). Every gate is an entry pad: stepping on it while the arena runs drops you at the
# landing point of the ACTIVE slot; only the active slot's exit works, and it puts you back at your team's gate (`out`).
# The active slot is re-rolled at random every `gate.every` ticks (V2: a 16-item hopper clock, 128 ticks). Entry sound to everyone.
#   gates: [{team, x y z = pad centre block (the pad itself is built by the map), out:{x,y,z,yaw}}]
#   slots: [{land:{x,y,z,yaw}, exit:{x,y,z = block the feet go in}}]
# Empty lists = no gates (a map or demo fills them through #nonios:arena/config).
data modify storage nonios:arena config.gate set value {every:128,sound:"minecraft:block.end_portal.spawn"}
data modify storage nonios:arena config.gates set value []
data modify storage nonios:arena config.slots set value []
# Core (V2 regrowing central block): config.core {x,y,z} = the block; while the arena runs, once it is mined (air) a new
# block is rolled from core_blocks (weights w) `core_regrow` ticks later (0 = next 10-tick check; V2 refilled it at once).
# V2 odds (two 9-slot dispenser rolls): cobblestone 4/9, log 2/9, hay 1/9, ore 2/9 -> emerald ore 8/9, emerald block 1/9 (x81).
# No config.core = no core.
data remove storage nonios:arena config.core
data modify storage nonios:arena config.core_regrow set value 0
data modify storage nonios:arena config.core_blocks set value [{id:"minecraft:cobblestone",w:36},{id:"minecraft:oak_log",w:18},{id:"minecraft:hay_block",w:9},{id:"minecraft:emerald_ore",w:16},{id:"minecraft:emerald_block",w:2}]
# Centre generator (feedback #39/#40): config.cgen {x,y,z} = the spot on top of its sea lantern (arena/setup builds the
# 3x3 base). Tuning comes from src/generators.json "centre" (tools/build_generators.py -> arena/cgen/config).
# No config.cgen = none.
data remove storage nonios:arena config.cgen
# Protection (feedback #43): config.protect {x1,y1,z1,x2,y2,z2, by = backup copy's lowest y}: every non-air block of
# that box at setup time is restored within a tick when broken (the core stays changeable).
# protect_types = purse coin blocks among them (their mining stat is cancelled so they pay nothing). None = off.
data remove storage nonios:arena config.protect
data modify storage nonios:arena config.protect_types set value []
