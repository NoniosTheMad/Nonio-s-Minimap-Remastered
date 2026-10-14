# as the player: build the shop dialog in storage nonios:shop ui.d (the section menu, or page nx.shop_sec - 1), then show it
execute store result score #bal nx.tmp run scoreboard players get @s nx.coins
execute store result storage nonios:shop ui.a.bal int 1 run scoreboard players get #bal nx.tmp
data modify storage nonios:shop ui.d set value {type:"minecraft:multi_action",title:{text:"Shop",color:"gold",bold:true},body:[],actions:[],columns:2,pause:false,after_action:"wait_for_response",exit_action:{label:"Close"}}
scoreboard players add @s nx.shop_sec 0
data remove storage nonios:shop ui.s
execute if score @s nx.shop_sec matches 1.. run function nonios:shop/ui/page
execute unless data storage nonios:shop ui.s run scoreboard players set @s nx.shop_sec 0
function nonios:shop/ui/balance with storage nonios:shop ui.a
data modify storage nonios:shop ui.d.body append from storage nonios:shop ui.msg
execute unless data storage nonios:shop ui.s run data modify storage nonios:shop ui.d.actions set from storage nonios:shop menu
execute if data storage nonios:shop ui.s run function nonios:shop/ui/page_actions
function nonios:shop/ui/show with storage nonios:shop ui
