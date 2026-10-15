# storage nonios:arena config -> scores (cheap; does not touch the nodes: run setup for that)
execute store result score #capture nx.arena run data get storage nonios:arena config.capture
scoreboard players operation #ncap nx.arena = #capture nx.arena
scoreboard players operation #ncap nx.arena *= #-1 nx.arena
execute store result score #step nx.arena run data get storage nonios:arena config.step
execute store result score #max_mult nx.arena run data get storage nonios:arena config.max_mult
execute store result score #decay nx.arena run data get storage nonios:arena config.decay
# runes: bar / rune resolution = capture x 10; redraw intervals
scoreboard players operation #cap10 nx.arena = #capture nx.arena
scoreboard players operation #cap10 nx.arena *= #10 nx.arena
execute store result score #rn_every nx.arena run data get storage nonios:arena config.rune.every
execute if score #rn_every nx.arena matches ..0 run scoreboard players set #rn_every nx.arena 3
execute store result score #rn_every_cap nx.arena run data get storage nonios:arena config.rune.every_cap
execute if score #rn_every_cap nx.arena matches ..0 run scoreboard players set #rn_every_cap nx.arena 2
execute store result score #int_pm nx.arena run data get storage nonios:arena config.interest_permille
execute store result score #int_cap nx.arena run data get storage nonios:arena config.interest_cap
execute store result score #ev_first nx.arena run data get storage nonios:arena config.event_first
execute store result score #ev_every nx.arena run data get storage nonios:arena config.event_every
execute store result score #ev_warn nx.arena run data get storage nonios:arena config.event_warn
execute store result score #trolls nx.arena run data get storage nonios:arena config.trolls
execute store result score #surge_waves nx.arena run data get storage nonios:arena config.surge_waves
execute store result score #frogs nx.arena run data get storage nonios:arena config.frogs
execute store result score #frog_life nx.arena run data get storage nonios:arena config.frog_life
execute store result score #golden_time nx.arena run data get storage nonios:arena config.golden_time
execute store result score #golden_mult nx.arena run data get storage nonios:arena config.golden_mult
execute store result score #bounty_time nx.arena run data get storage nonios:arena config.bounty_time
execute store result score #bounty_coins nx.arena run data get storage nonios:arena config.bounty_coins
execute store result score #grav_time nx.arena run data get storage nonios:arena config.gravity_time
execute store result score #lt_every nx.arena run data get storage nonios:arena config.lightning.every
execute store result score #lt_resp nx.arena run data get storage nonios:arena config.lightning.respawn
# lightning: the runtime switch (#lt_set, set by lightning/on|off) wins over the config default
execute store result score #lt_on nx.arena run data get storage nonios:arena config.lightning.on
execute if score #lt_set nx.arena matches 0..1 run scoreboard players operation #lt_on nx.arena = #lt_set nx.arena
function nonios:arena/event/sum_weights
# gates + core
execute store result score #g_every nx.arena run data get storage nonios:arena config.gate.every
execute if score #g_every nx.arena matches ..0 run scoreboard players set #g_every nx.arena 128
execute store result score #c_regrow nx.arena run data get storage nonios:arena config.core_regrow
function nonios:arena/core/sum_weights
