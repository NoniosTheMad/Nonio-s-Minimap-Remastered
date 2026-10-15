# macro {i}: fire config.events[i] at once, without the announcement countdown (demos)
scoreboard players set #ev_now nx.arena 1
$function nonios:arena/event/start {i:$(i)}
scoreboard players set #ev_now nx.arena 0
