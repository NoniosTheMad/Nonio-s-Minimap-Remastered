# storage nonios:arena config -> scores (cheap; does not touch the nodes: run setup for that)
execute store result score #capture nx.arena run data get storage nonios:arena config.capture
scoreboard players operation #ncap nx.arena = #capture nx.arena
scoreboard players operation #ncap nx.arena *= #-1 nx.arena
execute store result score #step nx.arena run data get storage nonios:arena config.step
execute store result score #max_mult nx.arena run data get storage nonios:arena config.max_mult
execute store result score #decay nx.arena run data get storage nonios:arena config.decay
execute store result score #per_roll nx.arena run data get storage nonios:arena config.per_roll
execute if score #per_roll nx.arena matches ..0 run scoreboard players set #per_roll nx.arena 4
execute store result score #item_cap nx.arena run data get storage nonios:arena config.item_cap
execute store result score #coins nx.arena run data get storage nonios:arena config.coins
execute store result score #indicator nx.arena run data get storage nonios:arena config.indicator
execute store result score #ev_first nx.arena run data get storage nonios:arena config.event_first
execute store result score #ev_every nx.arena run data get storage nonios:arena config.event_every
execute store result score #surge_waves nx.arena run data get storage nonios:arena config.surge_waves
execute store result score #frogs nx.arena run data get storage nonios:arena config.frogs
execute store result score #frog_life nx.arena run data get storage nonios:arena config.frog_life
execute store result score #golden_time nx.arena run data get storage nonios:arena config.golden_time
execute store result score #golden_mult nx.arena run data get storage nonios:arena config.golden_mult
execute store result score #lt_every nx.arena run data get storage nonios:arena config.lightning.every
execute store result score #lt_resp nx.arena run data get storage nonios:arena config.lightning.respawn
# lightning: the runtime switch (#lt_set, set by lightning/on|off) wins over the config default
execute store result score #lt_on nx.arena run data get storage nonios:arena config.lightning.on
execute if score #lt_set nx.arena matches 0..1 run scoreboard players operation #lt_on nx.arena = #lt_set nx.arena
function nonios:arena/event/sum_weights
