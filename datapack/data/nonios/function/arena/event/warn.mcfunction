# macro (storage ev): the announcement. Countdown bossbar to everyone, raid horn, a short title.
$bossbar set nonios:arena/event color $(bar)
execute store result bossbar nonios:arena/event max run scoreboard players get #ev_warn nx.arena
execute store result bossbar nonios:arena/event value run scoreboard players get #ev_wait nx.arena
bossbar set nonios:arena/event players @a
bossbar set nonios:arena/event visible true
function nonios:arena/event/bar_sec
function nonios:arena/event/mark
title @a times 5 50 15
title @a title ""
$title @a subtitle [{text:"$(name)",color:"$(color)",bold:true},{text:"  $(where)",color:"yellow",bold:false}]
execute as @a at @s run playsound minecraft:event.raid.horn master @s ~ ~ ~ 0.5 1
