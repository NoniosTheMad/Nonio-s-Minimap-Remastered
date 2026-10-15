# EVENT (as + at a node): a fountain of emeralds, surge_waves waves 6 ticks apart
tag @s add nx.surge
scoreboard players operation @s nx.ar_ev = #surge_waves nx.arena
schedule function nonios:arena/event/surge_wave 1t replace
