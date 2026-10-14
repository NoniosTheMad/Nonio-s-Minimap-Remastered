# row 1: Prev | Back | Next | Buy again (greyed when there is nowhere to go / nothing to repeat)
execute if score @s nx.shop_pg matches 1.. run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.prev
execute unless score @s nx.shop_pg matches 1.. run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.prev_off
execute if score @s nx.shop_sec matches 1.. run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.back
execute unless score @s nx.shop_sec matches 1.. run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.back_off
scoreboard players operation #last nx.tmp = #np nx.tmp
scoreboard players remove #last nx.tmp 1
execute if score @s nx.shop_pg < #last nx.tmp run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.next
execute unless score @s nx.shop_pg < #last nx.tmp run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.next_off
function nonios:shop/ui/again
