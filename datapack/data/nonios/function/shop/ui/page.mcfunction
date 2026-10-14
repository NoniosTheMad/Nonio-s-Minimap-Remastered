# ui.s = sections[nx.shop_sec - 1] (absent if out of range): title + Shop Keeper line
scoreboard players operation #k nx.tmp = @s nx.shop_sec
execute store result storage nonios:shop arg.k int 1 run scoreboard players remove #k nx.tmp 1
function nonios:shop/ui/pick_page with storage nonios:shop arg
execute unless data storage nonios:shop ui.s run return 0
data modify storage nonios:shop ui.d.title set from storage nonios:shop ui.s.title
data modify storage nonios:shop ui.d.body append from storage nonios:shop ui.s.body
