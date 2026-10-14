# as the player: drop its current class (class undo hook, every class item incl. locked armour, vision). Keeps nx.cls_basic.
function nonios:class/gen/strip
clear @s *[minecraft:custom_data~{nx_cls_item:true}]
scoreboard players set @s nx.class 0
scoreboard players set @s nx.tier 0
scoreboard players set @s nx.cls_restock 0
