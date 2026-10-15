# {key}: flip a 0b/1b flag in storage nonios:config
$execute store result score #c nx.tmp run data get storage nonios:config $(key)
$execute if score #c nx.tmp matches 1 run return run data modify storage nonios:config $(key) set value 0b
$data modify storage nonios:config $(key) set value 1b
