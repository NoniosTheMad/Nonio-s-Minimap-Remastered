scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[type=text_display,tag=nx.ang_halo] if score @s nx.pid = #me nx.cls_tmp run kill @s
