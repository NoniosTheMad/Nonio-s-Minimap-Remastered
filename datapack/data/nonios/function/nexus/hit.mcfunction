# damage = attacker's attack_damage x10 (sword ~70, fist 10). Teammates do nothing.
execute on attacker run tag @s add nx.attacker
$execute if entity @a[tag=nx.attacker,team=$(team)] run return run function nonios:nexus/hit_own
execute on attacker store result score #dmg nx.const run attribute @s minecraft:attack_damage get 10
scoreboard players operation @s nx.hp -= #dmg nx.const
# stats: barrier damage dealt this match (end-of-match summary)
execute on attacker run scoreboard players operation @s[type=player] nx.nxdmg += #dmg nx.const
scoreboard players operation @s nx.cd = #regen_delay nx.const
$function nonios:nexus/fx/pulse with storage nonios:nexus team.$(team)
$execute if score @s nx.alert matches 0 run function nonios:nexus/alert {team:"$(team)"}
$execute if score @s nx.hp matches ..0 run return run function nonios:nexus/broken {team:"$(team)"}
# explain to the attacker why the obsidian doesn't break (rate-limited per player)
execute on attacker if function nonios:nexus/msg_gate run function nonios:nexus/msg {m:'[{"text":"⛨ The Barrier protects the Nexus","color":"aqua"},{"text":" — break it first","color":"gray"}]'}
function nonios:nexus/hit_end
