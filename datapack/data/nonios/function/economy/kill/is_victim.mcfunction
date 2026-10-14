# as a player: succeeds if they are dead and their last attacker is the killer (tag nx.k.killer)
execute store result score #hp nx.eco run data get entity @s Health 100
execute if score #hp nx.eco matches 1.. run return fail
execute on attacker if entity @s[tag=nx.k.killer] run return 1
return fail
