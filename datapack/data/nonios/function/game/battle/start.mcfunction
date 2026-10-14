scoreboard players set #state nx.state 2
scoreboard players set #timer nx.state 0
function nonios:map/walls/down
function nonios:arena/start
function nonios:nexus/press/start
bossbar set nonios:phase color red
bossbar set nonios:phase max 1
bossbar set nonios:phase value 1
bossbar set nonios:phase name {"text":"⚔ Battle","color":"red"}
bossbar set nonios:phase players @a
title @a times 10 60 20
title @a subtitle {"text":"The Arena is open. Destroy the enemy Nexus!","color":"gray"}
title @a title {"text":"BARRIERS BROKEN","color":"red","bold":true}
execute as @a at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.6 1
execute as @a at @s run playsound minecraft:entity.generic.explode master @s ~ ~ ~ 1 0.6
