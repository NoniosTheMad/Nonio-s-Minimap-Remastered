# Champion (remaster shop class): starts at 0, grows with every player kill until it dies
scoreboard players set @s nx.cls_champ 0
function nonios:class/champion/level
playsound minecraft:item.armor.equip_gold player @a ~ ~ ~ 1 0.8
