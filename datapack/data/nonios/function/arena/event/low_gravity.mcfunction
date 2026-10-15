# EVENT (global): for gravity_time ticks everyone in the Arena jumps high and falls slowly
scoreboard players operation #grav_t nx.arena = #grav_time nx.arena
scoreboard players operation #ev_run nx.arena = #grav_time nx.arena
function nonios:arena/event/gravity_apply with storage nonios:arena config.bounds
