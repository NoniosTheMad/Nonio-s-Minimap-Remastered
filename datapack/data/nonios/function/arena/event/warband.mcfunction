# EVENT (global): WARBAND. config.warband {waves, size, gap, life, range}: `waves` waves of `size` raiders (vindicators,
# every 3rd a pillager; enemies of both teams) claw out of the ground within `range` of config.center, one wave every
# `gap` ticks. Each drops emeralds (loot nonios:arena/raider). Survivors leave after `life` ticks.
execute store result score #wb_waves nx.arena run data get storage nonios:arena config.warband.waves
execute store result score #wb_t nx.arena run data get storage nonios:arena config.warband.life
scoreboard players set #wb_next nx.arena 0
scoreboard players operation #ev_run nx.arena = #wb_t nx.arena
scoreboard players set #mob_ev nx.arena 1
