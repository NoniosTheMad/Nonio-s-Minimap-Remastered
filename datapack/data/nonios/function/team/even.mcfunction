execute store result score #w nx.tmp if entity @a[team=white]
execute store result score #b nx.tmp if entity @a[team=black]
scoreboard players operation #d nx.tmp = #w nx.tmp
scoreboard players operation #d nx.tmp -= #b nx.tmp
execute if score #d nx.tmp matches 2.. as @r[team=white] run return run function nonios:team/move {team:"black",Team:"Black",color:"light_purple"}
execute if score #d nx.tmp matches ..-2 as @r[team=black] run return run function nonios:team/move {team:"white",Team:"White",color:"white"}
