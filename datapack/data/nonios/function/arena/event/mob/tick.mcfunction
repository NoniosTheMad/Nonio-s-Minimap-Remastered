# every tick while an enemy event runs (event/tick). Timers count game ticks x #speed.
execute if score #wb_t nx.arena matches 1.. run function nonios:arena/event/mob/wb_tick
execute if score #wd_t nx.arena matches 1.. run function nonios:arena/event/mob/wd_tick
execute if score #gr_t nx.arena matches 1.. run function nonios:arena/event/mob/gr_tick
# once a second: event mobs that wandered out of the Arena go back to its centre
execute store result score #mt nx.arena run time query gametime
scoreboard players operation #mt nx.arena %= #20 nx.arena
execute if score #mt nx.arena matches 0 run function nonios:arena/event/mob/leash with storage nonios:arena config.bounds
execute unless score #wb_t nx.arena matches 1.. unless score #wd_t nx.arena matches 1.. unless score #gr_t nx.arena matches 1.. run scoreboard players set #mob_ev nx.arena 0
