# vanilla can't clear an item cooldown: re-give the class items in the other cooldown group (nx.cls_cdalt toggles)
execute store success score #c nx.cls_tmp if score @s nx.cls_cdalt matches 1
execute if score #c nx.cls_tmp matches 1 run scoreboard players set @s nx.cls_cdalt 0
execute if score #c nx.cls_tmp matches 0 run scoreboard players set @s nx.cls_cdalt 1
execute if score @s nx.class matches 1.. run clear @s *[minecraft:custom_data~{nx_cls_item:true}]
execute if score @s nx.class matches 1.. run function nonios:class/gen/check
execute if score @s nx.class matches 1 run scoreboard players set @s nx.cls_souls 5
execute if score @s nx.class matches 2 run scoreboard players set @s nx.cls_fuel 60
function demo:say {m:"Cooldowns reset (items re-given), 5 souls, broom full"}
