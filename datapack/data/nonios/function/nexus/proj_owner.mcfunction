# as a projectile; macro $(team) = the Barrier's team. #ao nx.tmp = 1 if it was shot by a player of the other team.
scoreboard players set #ao nx.tmp 0
$execute on owner if entity @s[type=player,team=!$(team)] run scoreboard players set #ao nx.tmp 1
