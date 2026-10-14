# as the player: #lvl nx.cls_tmp = its team's basic-class level (1-3). Team upgrades write #white / #black nx.cls_lvl.
scoreboard players operation #lvl nx.cls_tmp = #solo nx.cls_lvl
execute if entity @s[team=white] run scoreboard players operation #lvl nx.cls_tmp = #white nx.cls_lvl
execute if entity @s[team=black] run scoreboard players operation #lvl nx.cls_tmp = #black nx.cls_lvl
execute if score #lvl nx.cls_tmp matches ..0 run scoreboard players set #lvl nx.cls_tmp 1
execute if score #lvl nx.cls_tmp matches 4.. run scoreboard players set #lvl nx.cls_tmp 3
