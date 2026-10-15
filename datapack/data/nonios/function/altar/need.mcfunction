# {i}: cost of step i (reaching level i+1) into #ni / #ng / #nd nx.altar
$execute store result score #ni nx.altar run data get storage nonios:config altar_steps[$(i)].iron
$execute store result score #ng nx.altar run data get storage nonios:config altar_steps[$(i)].gold
$execute store result score #nd nx.altar run data get storage nonios:config altar_steps[$(i)].diamond
