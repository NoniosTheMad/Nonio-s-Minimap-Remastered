# {team}, from bank/interest/team every tick: #i nx.eco = the team bank's interest this tick (1 coin = #ithr).
# #tacc_<team> nx.talis collects it talisman_mult times; each #tth (= #ithr / 10, 0.1 coin) pays every holder of
# that team 0.1 coin. Adding #i once per round keeps it inside an int (the interest maths bound #i + #ithr).
execute store result score #tm nx.talis run data get storage nonios:config talisman_mult
scoreboard players set #ts nx.talis 0
$execute if score #tm nx.talis matches 1.. run function nonios:talisman/round {team:"$(team)"}
execute if score #ts nx.talis matches ..0 run return 0
scoreboard players operation #ts nx.talis *= #10 nx.talis
$execute as @a[team=$(team),gamemode=!spectator] if items entity @s armor.head *[minecraft:custom_data~{nx_talisman:1b}] run function nonios:talisman/pay
