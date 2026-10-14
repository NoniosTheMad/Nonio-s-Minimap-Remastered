# screen name, plus "n/N" when it has several pages
data modify storage nonios:shop ui.t set value {}
data modify storage nonios:shop ui.t.name set from storage nonios:shop ui.node.name
execute store result storage nonios:shop ui.t.p int 1 run scoreboard players add @s nx.shop_pg 1
scoreboard players remove @s nx.shop_pg 1
execute store result storage nonios:shop ui.t.np int 1 run scoreboard players get #np nx.tmp
execute if score #np nx.tmp matches 2.. run return run function nonios:shop/ui/title_pg with storage nonios:shop ui.t
function nonios:shop/ui/title_1 with storage nonios:shop ui.t
