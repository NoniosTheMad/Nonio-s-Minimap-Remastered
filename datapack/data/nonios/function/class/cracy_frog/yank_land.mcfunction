# landed: damage = blocks fallen from the peak down to max(landing, launch) - 3, at most 6 (3 hearts).
# Below the launch point vanilla fall damage still applies on top (it starts counting there).
execute if entity @s[tag=nx.frog_hooked] run return run function nonios:class/cracy_frog/hook_land
scoreboard players operation #fl nx.cls_tmp = #y nx.cls_tmp
execute if score #fl nx.cls_tmp < @s nx.cls_y0 run scoreboard players operation #fl nx.cls_tmp = @s nx.cls_y0
scoreboard players operation #d nx.cls_tmp = @s nx.cls_ypk
scoreboard players operation #d nx.cls_tmp -= #fl nx.cls_tmp
scoreboard players operation #d nx.cls_tmp /= #10 nx.cls_tmp
scoreboard players remove #d nx.cls_tmp 3
execute if score #d nx.cls_tmp matches 7.. run scoreboard players set #d nx.cls_tmp 6
execute store result storage nonios:class tmp.d int 1 run scoreboard players get #d nx.cls_tmp
execute if score #d nx.cls_tmp matches 1.. run function nonios:class/cracy_frog/yank_hurt with storage nonios:class tmp
function nonios:class/cracy_frog/yank_end
