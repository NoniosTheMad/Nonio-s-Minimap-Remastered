# the broom (mount + display) of the frog whose pid is in #me nx.cls_tmp
execute as @e[type=happy_ghast,tag=nx.frog_mount] if score @s nx.pid = #me nx.cls_tmp run tp @s ~ -300 ~
execute as @e[type=happy_ghast,tag=nx.frog_mount] if score @s nx.pid = #me nx.cls_tmp run kill @s
execute as @e[type=item_display,tag=nx.frog_broomfx] if score @s nx.pid = #me nx.cls_tmp run kill @s
