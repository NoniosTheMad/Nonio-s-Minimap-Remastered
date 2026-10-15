# EVENT (global): for golden_time ticks the centre generator runs golden_speed x faster (arena/cgen) and the
# interest node pays x golden_mult
scoreboard players operation #mult nx.arena = #golden_mult nx.arena
scoreboard players operation #golden_t nx.arena = #golden_time nx.arena
scoreboard players operation #ev_run nx.arena = #golden_time nx.arena
