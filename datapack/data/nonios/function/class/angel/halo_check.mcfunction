# class/second, as a halo: gone when its Angel is (offline, class lost)
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @a[scores={nx.class=12}] if score @s nx.pid = #me nx.cls_tmp run return 1
kill @s
