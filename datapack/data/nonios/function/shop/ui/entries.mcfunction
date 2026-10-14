# an items page: one button per entry of ui.list
execute unless data storage nonios:shop ui.list[0] run return 0
data modify storage nonios:shop ui.c set from storage nonios:shop ui.list[0]
data remove storage nonios:shop ui.list[0]
function nonios:shop/ui/entry
function nonios:shop/ui/button with storage nonios:shop ui.c
scoreboard players add #ne nx.tmp 1
function nonios:shop/ui/entries
