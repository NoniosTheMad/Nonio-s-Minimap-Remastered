# Classes page: one button per class entry of items (class/gen/shop_items); button sends nx.shop = 100 + index; price red when unaffordable
execute unless data storage nonios:shop ui.tmp[0] run return 0
data modify storage nonios:shop ui.c set from storage nonios:shop ui.tmp[0]
data remove storage nonios:shop ui.tmp[0]
scoreboard players add #n nx.tmp 1
execute unless data storage nonios:shop ui.c.class run return run function nonios:shop/ui/each
# a class sold under another label on another page (alias, e.g. Monster Skull) is listed there, not here
execute if data storage nonios:shop ui.c.alias run return run function nonios:shop/ui/each
execute store result storage nonios:shop ui.c.n int 1 run scoreboard players get #n nx.tmp
execute unless data storage nonios:shop ui.c.atlas run data modify storage nonios:shop ui.c.atlas set value "minecraft:items"
function nonios:shop/ui/afford
function nonios:shop/ui/action_class with storage nonios:shop ui.c
function nonios:shop/ui/each
