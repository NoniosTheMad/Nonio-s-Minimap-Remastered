scoreboard players add @s nx.class 0
scoreboard players add @s nx.cls_basic 0
scoreboard players add @s nx.cls_souls 0
scoreboard players add @s nx.cls_fuel 0
tellraw @s [{"text":"[demo] class ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.class"},"color":"white"},{"text":" (1 Reaper, 2 Cracy Frog, 3 Warrior), basic ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_basic"},"color":"white"},{"text":", team level ","color":"dark_purple"},{"score":{"name":"#solo","objective":"nx.cls_lvl"},"color":"white"},{"text":", souls ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_souls"},"color":"white"},{"text":", broom ","color":"dark_purple"},{"score":{"name":"@s","objective":"nx.cls_fuel"},"color":"white"},{"text":"/60","color":"dark_purple"}]
