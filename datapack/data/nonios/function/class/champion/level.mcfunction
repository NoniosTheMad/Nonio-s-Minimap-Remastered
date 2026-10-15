# as the Champion: max health and damage follow the streak (nx.cls_champ 0..5): +2 HP and +0.5 damage per kill
execute store result storage nonios:class tmp.hp int 2 run scoreboard players get @s nx.cls_champ
execute store result storage nonios:class tmp.dmg double 0.5 run scoreboard players get @s nx.cls_champ
function nonios:class/champion/mods with storage nonios:class tmp
