# EVENT (global): for bounty_time ticks every kill inside the Arena bounds pays bounty_coins extra (event/bounty_bonus,
# an #nonios:economy/kill_bonus entry)
scoreboard players operation #bounty_t nx.arena = #bounty_time nx.arena
scoreboard players operation #ev_run nx.arena = #bounty_time nx.arena
