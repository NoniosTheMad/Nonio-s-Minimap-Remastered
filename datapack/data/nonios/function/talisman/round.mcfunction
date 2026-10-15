# {team}: one talisman_mult round of talisman/accrue (#tm rounds left)
$scoreboard players operation #tacc_$(team) nx.talis += #i nx.eco
$scoreboard players operation #tq nx.talis = #tacc_$(team) nx.talis
scoreboard players operation #tq nx.talis /= #tth nx.eco
$scoreboard players operation #tacc_$(team) nx.talis %= #tth nx.eco
scoreboard players operation #ts nx.talis += #tq nx.talis
scoreboard players remove #tm nx.talis 1
$execute if score #tm nx.talis matches 1.. run function nonios:talisman/round {team:"$(team)"}
