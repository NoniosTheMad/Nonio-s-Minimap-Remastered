# a half-block step of the lantern's aim: the first living enemy whose box comes within ~half a block is bound
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,tag=!nx.cls_me,tag=!nx.cls_ally,type=!#nonios:class/tongue_ignore,limit=1] if data entity @s Health unless entity @s[type=player,gamemode=!survival,gamemode=!adventure] run return run tag @s add nx.reaper_bindhit
scoreboard players add #r nx.cls_tmp 1
execute if score #r nx.cls_tmp matches 16.. run return 0
execute positioned ^ ^ ^0.5 if block ~ ~ ~ #nonios:class/angel_ray run function nonios:class/reaper/bind_ray
