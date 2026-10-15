scoreboard players set #wd_t nx.arena 0
# the bar is the Warden's only while it is the current event
execute if data storage nonios:arena ev{id:"warden"} run scoreboard players set #ev_run nx.arena 0
execute if data storage nonios:arena ev{id:"warden"} run bossbar set nonios:arena/event visible false
title @a times 5 50 15
title @a title ""
title @a subtitle {text:"The Gilded Warden has fallen",color:"gold"}
execute as @a at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 0.8 0.8
execute at @e[type=marker,tag=nx.ev_guard] run particle minecraft:totem_of_undying ~ ~1 ~ 0.8 1 0.8 0.5 60
kill @e[type=marker,tag=nx.ev_guard]
