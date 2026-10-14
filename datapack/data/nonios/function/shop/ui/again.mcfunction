# "buy again": icon of the last purchase, its quantity and price now (greyed if unaffordable or nothing bought yet)
execute unless score @s nx.shop_last matches 1.. run return run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.again_off
execute store result storage nonios:shop arg.i int 1 run scoreboard players remove @s nx.shop_last 1
scoreboard players add @s nx.shop_last 1
data remove storage nonios:shop ui.c
function nonios:shop/ui/pick_c with storage nonios:shop arg
execute unless data storage nonios:shop ui.c run return run data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.again_off
scoreboard players set #again nx.tmp 1
function nonios:shop/ui/entry
scoreboard players set #again nx.tmp 0
data modify storage nonios:shop ui.c.label set from storage nonios:shop ui.c.name
execute if data storage nonios:shop ui.c{act:0b} run return run function nonios:shop/ui/again_btn_off with storage nonios:shop ui.c
function nonios:shop/ui/again_btn with storage nonios:shop ui.c
