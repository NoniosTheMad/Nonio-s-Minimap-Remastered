# #p = price x #lots (sel.tot); sel.count = items handed out = base count x #lots (sel.q for messages).
# sel.base keeps the catalog count (total runs again when fewer lots fit).
execute store result score #p nx.tmp run data get storage nonios:shop sel.price
scoreboard players operation #p nx.tmp *= #lots nx.tmp
execute store result storage nonios:shop sel.tot int 1 run scoreboard players get #p nx.tmp
execute unless data storage nonios:shop sel.base run data modify storage nonios:shop sel.base set from storage nonios:shop sel.count
execute store result score #q nx.tmp run data get storage nonios:shop sel.base
scoreboard players operation #q nx.tmp *= #lots nx.tmp
execute store result storage nonios:shop sel.count int 1 run scoreboard players get #q nx.tmp
execute store result storage nonios:shop sel.q int 1 run scoreboard players get #q nx.tmp
