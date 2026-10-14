# ui.node = nodes[nx.shop_sec] (absent if out of range)
data remove storage nonios:shop ui.node
execute store result storage nonios:shop arg.k int 1 run scoreboard players get @s nx.shop_sec
function nonios:shop/ui/pick_node with storage nonios:shop arg
