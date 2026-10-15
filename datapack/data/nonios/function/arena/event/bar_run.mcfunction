# macro (storage ev): a timed event is running; the bar shows the time left (event/running counts it down)
$bossbar set nonios:arena/event name {text:"$(name)",color:"$(color)",bold:true}
$bossbar set nonios:arena/event color $(bar)
execute store result bossbar nonios:arena/event max run scoreboard players get #ev_run nx.arena
execute store result bossbar nonios:arena/event value run scoreboard players get #ev_run nx.arena
bossbar set nonios:arena/event players @a
bossbar set nonios:arena/event visible true
