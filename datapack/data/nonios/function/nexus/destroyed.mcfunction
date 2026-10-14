# as/at the core marker: the obsidian is gone. The breaker is whoever has a fresh nx.mn.obsidian (mined stat).
# Not allowed while the Barrier stands, nor by the Nexus' own team: put it back.
$execute if entity @e[type=interaction,tag=nx.shield,tag=nx.$(team),distance=..2] run return run function nonios:nexus/restore {why:"The Barrier still stands."}
$execute if entity @a[team=$(team),scores={nx.mn.obsidian=1..}] run return run function nonios:nexus/restore {why:"You can't break your own Nexus."}
$scoreboard players add @a[team=$(enemy),scores={nx.mn.obsidian=1..}] nx.nxkill 1
scoreboard players set @a[scores={nx.mn.obsidian=1..}] nx.mn.obsidian 0
$title @a title {"text":"$(Team) NEXUS DESTROYED","color":"gold","bold":true}
$title @a[team=$(team)] subtitle {"text":"No more respawns.","color":"red"}
playsound minecraft:entity.ender_dragon.death master @a ~ ~ ~ 1 1
$bossbar set nonios:barrier_$(team) visible false
$function nonios:game/nexus_lost {team:"$(team)"}
kill @s
