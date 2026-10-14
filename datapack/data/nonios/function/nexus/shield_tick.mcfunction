# as/at the shield interaction. Hits: interaction stores the last attack.
$execute if data entity @s attack run function nonios:nexus/hit {team:"$(team)",enemy:"$(enemy)"}
scoreboard players remove @s[scores={nx.cd=1..}] nx.cd 1
scoreboard players remove @s[scores={nx.alert=1..}] nx.alert 1
execute if score @s nx.cd matches 0 if score @s nx.hp < @s nx.hp_max run function nonios:nexus/regen
function nonios:nexus/fx/tick
$execute store result bossbar nonios:barrier_$(team) value run scoreboard players get @s nx.hp
$execute store result bossbar nonios:barrier_$(team) max run scoreboard players get @s nx.hp_max
# defenders always see their bar; anyone within 24 blocks sees it too
$tag @a remove nx.bar_$(team)
$tag @a[team=$(team)] add nx.bar_$(team)
$tag @a[distance=..24] add nx.bar_$(team)
$execute if entity @a[tag=nx.bar_$(team)] run bossbar set nonios:barrier_$(team) players @a[tag=nx.bar_$(team)]
$execute unless entity @a[tag=nx.bar_$(team)] run bossbar set nonios:barrier_$(team) players
