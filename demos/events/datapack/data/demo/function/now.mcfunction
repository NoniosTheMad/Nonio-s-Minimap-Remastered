# macro {i}: fire config.events[i] at once (no countdown)
execute unless score #on nx.arena matches 1 run function demo:battle
$function nonios:arena/event/now {i:$(i)}
