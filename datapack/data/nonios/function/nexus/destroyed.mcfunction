$title @a title {"text":"$(Team) NEXUS DESTROYED","color":"gold","bold":true}
$title @a[team=$(team)] subtitle {"text":"No more respawns.","color":"red"}
playsound minecraft:entity.ender_dragon.death master @a ~ ~ ~ 1 1
$bossbar set nonios:barrier_$(team) visible false
kill @s
