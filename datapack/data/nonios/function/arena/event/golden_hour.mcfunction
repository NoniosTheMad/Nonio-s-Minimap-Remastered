# EVENT (global, #127): for golden_time ticks every coin earned in the centre is x golden_mult: the centre generator's
# emeralds (arena/cgen/drop), kill rewards for kills inside the Arena box incl. bounty / streak bonuses
# (event/golden_kill via #nonios:economy/kill_mult) and the interest node's payout. Dropped / taken purses are not.
scoreboard players operation #mult nx.arena = #golden_mult nx.arena
scoreboard players operation #golden_t nx.arena = #golden_time nx.arena
scoreboard players operation #ev_run nx.arena = #golden_time nx.arena
