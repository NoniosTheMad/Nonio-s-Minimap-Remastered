# sel.lvl levels per lot
execute store result score #q nx.tmp run data get storage nonios:shop sel.lvl
scoreboard players operation #q nx.tmp *= #lots nx.tmp
execute store result storage nonios:shop sel.lv int 1 run scoreboard players get #q nx.tmp
scoreboard players operation @s nx.coins -= #p nx.tmp
function nonios:shop/xp_add with storage nonios:shop sel
function nonios:shop/paid
