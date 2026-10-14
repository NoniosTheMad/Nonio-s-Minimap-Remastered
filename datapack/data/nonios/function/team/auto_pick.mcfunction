# smaller team (White on a tie)
execute store result score #w nx.tmp if entity @a[team=white]
execute store result score #b nx.tmp if entity @a[team=black]
execute if entity @s[team=white] run scoreboard players remove #w nx.tmp 1
execute if entity @s[team=black] run scoreboard players remove #b nx.tmp 1
execute if score #w nx.tmp <= #b nx.tmp run return run function nonios:team/pick {team:"white",Team:"White",color:"white"}
function nonios:team/pick {team:"black",Team:"Black",color:"light_purple"}
