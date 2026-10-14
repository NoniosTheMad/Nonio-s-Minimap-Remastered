# #lots nx.tmp = how many lots of storage nonios:shop $(p) (sel or ui.c) a click buys: 1 unless it sells in bulk;
# else the quantity mode (x1 / x8 / x64 / Stack = sl lots), or the last purchase's lots when buying again.
scoreboard players set #lots nx.tmp 1
$execute unless data storage nonios:shop $(p){bulk:1} run return 0
execute if score #again nx.tmp matches 1 if score @s nx.shop_lastl matches 1.. run return run scoreboard players operation #lots nx.tmp = @s nx.shop_lastl
execute if score @s nx.shop_qm matches 1 run scoreboard players set #lots nx.tmp 8
execute if score @s nx.shop_qm matches 2 run scoreboard players set #lots nx.tmp 64
$execute if score @s nx.shop_qm matches 3 store result score #lots nx.tmp run data get storage nonios:shop $(p).sl
execute if score #lots nx.tmp matches ..0 run scoreboard players set #lots nx.tmp 1
