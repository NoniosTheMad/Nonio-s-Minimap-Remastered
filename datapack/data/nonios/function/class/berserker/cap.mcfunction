# max health -> the last allowed health (nx.cls_bhp) for 3 s
attribute @s minecraft:max_health modifier remove nonios:berserk_cap
scoreboard players operation #d nx.cls_tmp = @s nx.cls_bhp
scoreboard players operation #d nx.cls_tmp -= #mx nx.cls_tmp
execute store result storage nonios:tmp bz.a double 0.01 run scoreboard players get #d nx.cls_tmp
function nonios:class/berserker/cap_set with storage nonios:tmp bz
scoreboard players set @s nx.cls_bcap 60
