# as the player: build the shop dialog in storage nonios:shop ui.d from the catalog, then show it
execute store result score #bal nx.tmp run scoreboard players get @s nx.coins
execute store result storage nonios:shop ui.a.bal int 1 run scoreboard players get #bal nx.tmp
data modify storage nonios:shop ui.d set value {type:"minecraft:multi_action",title:{text:"Shop",color:"gold",bold:true},body:[],actions:[],columns:2,pause:false,after_action:"wait_for_response",exit_action:{label:"Close"}}
function nonios:shop/ui/balance with storage nonios:shop ui.a
data modify storage nonios:shop ui.d.body append from storage nonios:shop ui.msg
data modify storage nonios:shop ui.tmp set from storage nonios:shop items
scoreboard players set #n nx.tmp 99
function nonios:shop/ui/each
function nonios:shop/ui/show with storage nonios:shop ui
