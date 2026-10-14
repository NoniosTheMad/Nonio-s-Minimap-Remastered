# one button per catalog entry; button sends nx.shop = 100 + index; price shown red when the player can't afford it
execute unless data storage nonios:shop ui.tmp[0] run return 0
data modify storage nonios:shop ui.c set from storage nonios:shop ui.tmp[0]
data remove storage nonios:shop ui.tmp[0]
scoreboard players add #n nx.tmp 1
execute store result storage nonios:shop ui.c.n int 1 run scoreboard players get #n nx.tmp
execute unless data storage nonios:shop ui.c.atlas run data modify storage nonios:shop ui.c.atlas set value "minecraft:items"
execute store result score #p nx.tmp run data get storage nonios:shop ui.c.price
data modify storage nonios:shop ui.c.col set value "green"
data modify storage nonios:shop ui.c.tip set value "Click to buy"
execute if score #p nx.tmp > #bal nx.tmp run data modify storage nonios:shop ui.c.col set value "red"
execute if score #p nx.tmp > #bal nx.tmp run data modify storage nonios:shop ui.c.tip set value "Not enough coins"
function nonios:shop/ui/action with storage nonios:shop ui.c
function nonios:shop/ui/each
