# one half-block step of the tongue. Returns 1 when it is done (caught something or hit a block).
tp @s ^ ^ ^0.5
execute at @s run particle minecraft:dust{color:[0.95,0.45,0.6],scale:1.3} ~ ~ ~ 0 0 0 0 1 force
execute at @s unless block ~ ~ ~ #minecraft:replaceable run return run scoreboard players set @e[tag=nx.cls_me,limit=1] nx.cls_tng 0
execute at @s positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,tag=!nx.cls_me,tag=!nx.cls_ally,tag=!nx.frog_yanked,tag=!nx.frog_immune,type=!#nonios:class/tongue_ignore,sort=nearest,limit=1] if data entity @s Health unless entity @s[type=player,gamemode=!survival,gamemode=!adventure] run tag @s add nx.frog_hit
execute unless entity @e[tag=nx.frog_hit,limit=1] run return 0
scoreboard players set @e[tag=nx.cls_me,limit=1] nx.cls_tng 0
kill @s
return 1
