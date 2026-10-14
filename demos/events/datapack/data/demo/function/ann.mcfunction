# macro {i}: announce config.events[i] (countdown bar, then it fires); starts the battle first if needed
execute unless score #on nx.arena matches 1 run function demo:battle
$function nonios:arena/event/start {i:$(i)}
