# Angel, every tick: the beam lives while the staff is held up (angel/use_staff sets nx.cls_abm each tick)
execute if score @s nx.cls_abm matches 1.. run scoreboard players remove @s nx.cls_abm 1
execute if score @s nx.cls_abm matches 0 if score @s nx.cls_alk matches 1 run function nonios:class/angel/unlock
scoreboard players operation #me nx.cls_tmp = @s nx.pid
# the halo follows (teleport_duration smooths it)
execute as @e[type=text_display,tag=nx.ang_halo] if score @s nx.pid = #me nx.cls_tmp positioned ~ ~2.1 ~ run tp @s ~ ~ ~
# Sanctuary waves of this Angel
execute as @e[type=marker,tag=nx.ang_wave] if score @s nx.pid = #me nx.cls_tmp at @s run function nonios:class/angel/wave
