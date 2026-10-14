scoreboard players set #state nx.state 3
function nonios:arena/stop
function nonios:nexus/press/stop
execute store result score #timer nx.state run data get storage nonios:config end_time 20
execute store result bossbar nonios:phase max run data get storage nonios:config end_time
bossbar set nonios:phase color yellow
# the countdown name comes from end/tick once per second: replace the battle clock now, not a second later
execute store result bossbar nonios:phase value run data get storage nonios:config end_time
bossbar set nonios:phase name {"text":"Match over","color":"yellow"}
title @a times 10 80 20
gamemode adventure @a[gamemode=survival]
effect give @a minecraft:resistance infinite 4 true
