# row 2: quantity modes; the current one highlighted (applies to items sold in bulk, x1 for the rest)
execute if score @s nx.shop_qm matches 0 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m0s
execute unless score @s nx.shop_qm matches 0 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m0
execute if score @s nx.shop_qm matches 1 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m1s
execute unless score @s nx.shop_qm matches 1 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m1
execute if score @s nx.shop_qm matches 2 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m2s
execute unless score @s nx.shop_qm matches 2 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m2
execute if score @s nx.shop_qm matches 3 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m3s
execute unless score @s nx.shop_qm matches 3 run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.m3
