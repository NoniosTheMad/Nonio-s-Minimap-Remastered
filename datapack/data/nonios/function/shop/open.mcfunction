# as the player: build the shop screen in storage nonios:shop ui.d and show it. Layout (4 columns, positions never move):
#   title = screen name (+ page n/N); body = one line: purse + the last action's result
#   row 1: Prev | Back | Next | Buy again        row 2: x1 | x8 | x64 | Stack (current one highlighted)
#   rows 3-6: 16 slots (categories or items; empty slots padded). Unaffordable items are greyed out with their price.
execute store result score #bal nx.tmp run scoreboard players get @s nx.coins
scoreboard players add @s nx.shop_sec 0
scoreboard players add @s nx.shop_pg 0
scoreboard players add @s nx.shop_qm 0
function nonios:shop/ui/node_of_player
execute unless data storage nonios:shop ui.node run scoreboard players set @s nx.shop_sec 0
execute unless data storage nonios:shop ui.node run function nonios:shop/ui/node_of_player
execute store result score #np nx.tmp run data get storage nonios:shop ui.node.pages
execute if score @s nx.shop_pg >= #np nx.tmp run scoreboard players operation @s nx.shop_pg = #np nx.tmp
execute if score @s nx.shop_pg >= #np nx.tmp run scoreboard players remove @s nx.shop_pg 1
execute if score @s nx.shop_pg matches ..-1 run scoreboard players set @s nx.shop_pg 0
execute store result storage nonios:shop arg.p int 1 run scoreboard players get @s nx.shop_pg
function nonios:shop/ui/pick_list with storage nonios:shop arg
data modify storage nonios:shop ui.d set value {type:"minecraft:multi_action",title:"Shop",body:[],actions:[],columns:4,pause:false,after_action:"wait_for_response",exit_action:{label:"Close",width:120}}
function nonios:shop/ui/title
function nonios:shop/ui/body
function nonios:shop/ui/row_nav
function nonios:shop/ui/row_mode
scoreboard players set #ne nx.tmp 0
execute if data storage nonios:shop ui.node{kind:"menu"} run function nonios:shop/ui/menu
execute if data storage nonios:shop ui.node{kind:"items"} run function nonios:shop/ui/entries
function nonios:shop/ui/pad
function nonios:shop/ui/show with storage nonios:shop ui
