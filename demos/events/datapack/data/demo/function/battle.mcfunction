# start a match (if none) and skip the preparation: events only run in the battle
execute if score #state nx.state matches 0 run function demo:start
execute if score #state nx.state matches 1 run function nonios:game/battle/start
