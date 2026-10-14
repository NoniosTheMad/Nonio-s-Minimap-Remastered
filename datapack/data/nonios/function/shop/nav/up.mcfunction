# back to the parent screen, on the page that lists this one
function nonios:shop/ui/node_of_player
execute unless data storage nonios:shop ui.node run return run function nonios:shop/nav/go {j:0,p:0}
execute store result score @s nx.shop_sec run data get storage nonios:shop ui.node.up
execute store result score @s nx.shop_pg run data get storage nonios:shop ui.node.upg
