# a half-block step of the aim from the Angel's eyes: the first ally whose box comes within ~half a block is locked
execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[tag=nx.cls_ally,dx=0,dy=0,dz=0,limit=1] run return run function nonios:class/angel/lock
scoreboard players add #r nx.cls_tmp 1
execute if score #r nx.cls_tmp matches 32.. run return 0
execute positioned ^ ^ ^0.5 if block ~ ~ ~ #nonios:class/angel_ray run function nonios:class/angel/ray
