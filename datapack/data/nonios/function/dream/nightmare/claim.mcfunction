# reward of advancement nonios:dream/exodia (right-click on the altar). The first of each team to claim it gets Exodia.
advancement revoke @s only nonios:dream/exodia
execute at @s if entity @e[tag=nx.dream_nm,distance=..48] run return run function nonios:dream/nightmare/stirs
scoreboard players set #tm nx.dream 0
execute if entity @s[team=white] run scoreboard players set #tm nx.dream 1
execute if entity @s[team=black] run scoreboard players set #tm nx.dream 2
execute if score #tm nx.dream matches 1 if score #exodia_white nx.dream matches 1 run return run function nonios:dream/nightmare/taken
execute if score #tm nx.dream matches 2 if score #exodia_black nx.dream matches 1 run return run function nonios:dream/nightmare/taken
execute if score #tm nx.dream matches 0 if entity @s[tag=nx.exodia_claimed] run return run function nonios:dream/nightmare/taken
execute if score #tm nx.dream matches 1 run scoreboard players set #exodia_white nx.dream 1
execute if score #tm nx.dream matches 2 run scoreboard players set #exodia_black nx.dream 1
tag @s add nx.exodia_claimed
function #nonios:dream/exodia_grant
tellraw @a [{"selector":"@s","color":"dark_purple"},{"text":" has claimed Exodia.","color":"dark_purple"}]
execute at @s run playsound minecraft:ui.toast.challenge_complete master @a ~ ~ ~ 1 0.7
execute at @s run particle minecraft:sculk_soul ~ ~1 ~ 1 1 1 0.05 80
