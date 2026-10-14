# every arena loop while lightning is on
execute store result score #lr nx.arena if entity @e[type=rabbit,tag=nx.lrabbit]
execute if score #lr nx.arena matches 0 run function nonios:arena/lightning/wait
execute if score #lr nx.arena matches 1.. run function nonios:arena/lightning/active
