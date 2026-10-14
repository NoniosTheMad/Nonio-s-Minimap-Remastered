# damage = attacker's attack_damage x10 (sword ~70, fist 10). Teammates do nothing.
execute on attacker run tag @s add nx.attacker
$execute if entity @a[tag=nx.attacker,team=$(team)] run return run function nonios:nexus/hit_end
execute on attacker store result score #dmg nx.const run attribute @s minecraft:attack_damage get 10
scoreboard players operation @s nx.hp -= #dmg nx.const
scoreboard players operation @s nx.cd = #regen_delay nx.const
particle minecraft:electric_spark ~ ~0.6 ~ 0.4 0.4 0.4 0.2 25
playsound minecraft:block.amethyst_block.hit block @a ~ ~ ~ 1.5 0.6
$execute if score @s nx.alert matches 0 run function nonios:nexus/alert {team:"$(team)"}
$execute if score @s nx.hp matches ..0 run function nonios:nexus/broken {team:"$(team)"}
function nonios:nexus/hit_end
