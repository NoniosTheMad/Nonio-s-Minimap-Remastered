# catalog page: one button per entry of ui.s.items (n = button code, precomputed by tools/build_shop.py)
execute unless data storage nonios:shop ui.tmp[0] run return 0
data modify storage nonios:shop ui.c set from storage nonios:shop ui.tmp[0]
data remove storage nonios:shop ui.tmp[0]
function nonios:shop/ui/afford
function nonios:shop/ui/action with storage nonios:shop ui.c
function nonios:shop/ui/each_item
