# as/at the frog while its tongue is out: move it, resolve a hit (yank + spring away) or a miss
scoreboard players remove @s nx.cls_tng 1
scoreboard players operation #me nx.cls_tmp = @s nx.pid
tag @s add nx.cls_me
execute if entity @s[team=white] run tag @e[type=player,team=white] add nx.cls_ally
execute if entity @s[team=black] run tag @e[type=player,team=black] add nx.cls_ally
execute as @e[type=marker,tag=nx.frog_tongue] if score @s nx.pid = #me nx.cls_tmp at @s run function nonios:class/cracy_frog/tongue_step
execute as @e[tag=nx.frog_hit,limit=1] at @s run function nonios:class/cracy_frog/yank
execute if entity @e[tag=nx.frog_hit,limit=1] run function nonios:class/cracy_frog/spring
tag @e[tag=nx.frog_hit] remove nx.frog_hit
tag @e[tag=nx.cls_ally] remove nx.cls_ally
tag @s remove nx.cls_me
# out of reach or stopped by a wall: it just slaps back
execute if score @s nx.cls_tng matches ..0 as @e[type=marker,tag=nx.frog_tongue] if score @s nx.pid = #me nx.cls_tmp at @s run function nonios:class/cracy_frog/tongue_miss
