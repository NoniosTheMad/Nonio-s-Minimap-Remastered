# as/at the shield: #adm nx.tmp = this tick's projectile damage (nexus/proj_hit); shooters are tagged nx.arrow_shooter.
# Same as a melee hit (nexus/hit) at 20%: HP, regen delay, flash, alert, break.
scoreboard players operation @s nx.hp -= #adm nx.tmp
scoreboard players operation @s nx.cd = #regen_delay nx.const
$function nonios:nexus/fx/pulse with storage nonios:nexus team.$(team)
$execute if score @s nx.alert matches 0 run function nonios:nexus/alert {team:"$(team)"}
execute if score @s nx.hp matches ..0 run tag @a remove nx.arrow_shooter
$execute if score @s nx.hp matches ..0 run return run function nonios:nexus/broken {team:"$(team)"}
execute as @a[tag=nx.arrow_shooter] if function nonios:nexus/msg_gate run function nonios:nexus/msg {m:'{"text":"⛨ Nexus Barrier","color":"aqua"}'}
tag @a remove nx.arrow_shooter
