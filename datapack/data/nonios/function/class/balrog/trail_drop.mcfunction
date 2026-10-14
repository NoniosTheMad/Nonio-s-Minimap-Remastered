# as/at a Balrog: a trail marker at its feet (4.5 s) that remembers its team (team-mates are spared)
summon minecraft:marker ~ ~ ~ {Tags:["nx.bal_trail","nx.bal_new"]}
scoreboard players set @e[type=marker,tag=nx.bal_new] nx.cls_ttl 90
execute if entity @s[team=white] run tag @e[type=marker,tag=nx.bal_new] add nx.bal_white
execute if entity @s[team=black] run tag @e[type=marker,tag=nx.bal_new] add nx.bal_black
tag @e[type=marker,tag=nx.bal_new] remove nx.bal_new
