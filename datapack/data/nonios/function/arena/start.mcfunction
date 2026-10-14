# Start (or resume) the arena loop. Starting from stopped: the first event comes `event_first` ticks later.
execute unless score #on nx.arena matches 1 run scoreboard players operation #ev_t nx.arena = #ev_first nx.arena
scoreboard players set #on nx.arena 1
schedule function nonios:arena/loop 10t replace
function nonios:arena/gate/state
