# {key, op: add|remove, n, min, max} on an int in storage nonios:config
$execute store result score #c nx.tmp run data get storage nonios:config $(key)
$scoreboard players $(op) #c nx.tmp $(n)
$execute if score #c nx.tmp matches ..$(min) run scoreboard players set #c nx.tmp $(min)
$execute if score #c nx.tmp matches $(max).. run scoreboard players set #c nx.tmp $(max)
$execute store result storage nonios:config $(key) int 1 run scoreboard players get #c nx.tmp
