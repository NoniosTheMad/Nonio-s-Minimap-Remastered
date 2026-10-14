# basic-class team level +1 for my team (1-3, cycles), my basic class re-applied at once
execute if entity @s[team=black] run scoreboard players add #black nx.cls_lvl 1
execute if entity @s[team=black] if score #black nx.cls_lvl matches 4.. run scoreboard players set #black nx.cls_lvl 1
execute unless entity @s[team=black] run scoreboard players add #white nx.cls_lvl 1
execute unless entity @s[team=black] if score #white nx.cls_lvl matches 4.. run scoreboard players set #white nx.cls_lvl 1
scoreboard players operation #solo nx.cls_lvl = #white nx.cls_lvl
function nonios:class/level
tellraw @s [{"text":"[demo] Team class level ","color":"yellow"},{"score":{"name":"#lvl","objective":"nx.cls_tmp"},"color":"white"}]
execute if score @s nx.cls_basic matches 1.. if score @s nx.class = @s nx.cls_basic run function demo:reapply_basic
