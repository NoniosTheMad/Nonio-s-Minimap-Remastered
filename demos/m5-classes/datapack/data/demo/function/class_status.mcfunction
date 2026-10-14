scoreboard players add @s nx.class 0
scoreboard players add @s nx.tier 0
scoreboard players add @s nx.cls_basic 0
scoreboard players add @s nx.pdebt 0
function nonios:class/level
tellraw @s [{"text":"[demo] class ","color":"yellow"},{"score":{"name":"@s","objective":"nx.class"},"color":"white"},{"text":" (0 none, 1 Reaper, 2 Cracy Frog, 3 Warrior) | kill tier ","color":"yellow"},{"score":{"name":"@s","objective":"nx.tier"},"color":"white"},{"text":" | basic ","color":"yellow"},{"score":{"name":"@s","objective":"nx.cls_basic"},"color":"white"},{"text":" | team level ","color":"yellow"},{"score":{"name":"#lvl","objective":"nx.cls_tmp"},"color":"white"},{"text":" | purse ","color":"yellow"},{"score":{"name":"@s","objective":"nx.coins"},"color":"gold"},{"text":" | debt ","color":"yellow"},{"score":{"name":"@s","objective":"nx.pdebt"},"color":"red"}]
