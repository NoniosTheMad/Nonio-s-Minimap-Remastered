# as/at the shield interaction. Hits: interaction stores the last attack.
$execute if data entity @s attack run function nonios:nexus/hit {team:"$(team)",enemy:"$(enemy)"}
# projectiles (#37, #47): an enemy player's arrow / trident / firework / wind charge / fireball that flies into the
# shell deals 20% of its damage (nexus/proj, nexus/hit_arrow). #cx #cy #cz = the core's centre x100.
scoreboard players set #adm nx.tmp 0
execute store result score #cx nx.tmp run data get entity @s Pos[0] 100
execute store result score #cy nx.tmp run data get entity @s Pos[1] 100
scoreboard players add #cy nx.tmp 60
execute store result score #cz nx.tmp run data get entity @s Pos[2] 100
$execute as @e[type=#nonios:nexus_projectiles,distance=..10,tag=!nx.arrow_done] run function nonios:nexus/proj {team:"$(team)"}
$execute if score #adm nx.tmp matches 1.. run function nonios:nexus/hit_arrow {team:"$(team)"}
scoreboard players remove @s[scores={nx.cd=1..}] nx.cd 1
scoreboard players remove @s[scores={nx.alert=1..}] nx.alert 1
execute if score @s nx.cd matches 0 if score @s nx.hp < @s nx.hp_max run function nonios:nexus/regen
$function nonios:nexus/fx/tick {team:"$(team)"}
$execute store result bossbar nonios:barrier_$(team) value run scoreboard players get @s nx.hp
$execute store result bossbar nonios:barrier_$(team) max run scoreboard players get @s nx.hp_max
# only the barrier's own team sees the bar (attackers read the shell + the actionbar HP on hit)
$execute if entity @a[team=$(team),limit=1] run bossbar set nonios:barrier_$(team) players @a[team=$(team)]
$execute unless entity @a[team=$(team),limit=1] run bossbar set nonios:barrier_$(team) players
