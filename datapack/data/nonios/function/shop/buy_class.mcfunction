# as the buyer; storage nonios:shop sel = a class entry {name,class,num,price,ptxt,confirm} (class/gen/shop_items)
$execute if score @s nx.class matches $(num) run return run data modify storage nonios:shop ui.msg set value {type:"minecraft:plain_message",width:300,contents:{text:"✘ You already are the $(name).",color:"red"}}
execute store result score #p nx.tmp run data get storage nonios:shop sel.price
execute if score @s nx.coins < #p nx.tmp run return run function nonios:shop/broke
# free classes behind a confirmation (Cracy Frog's three questions): the dialog chain applies the class
$scoreboard players set @s nx.cls_req $(num)
execute if data storage nonios:shop sel{confirm:1} run scoreboard players set #noopen nx.tmp 1
execute if data storage nonios:shop sel{confirm:1} run return run function nonios:class/gen/confirm
scoreboard players operation @s nx.coins -= #p nx.tmp
$function nonios:class/set_id {id:"$(class)"}
playsound minecraft:entity.villager.yes master @s ~ ~ ~ 0.6 1
$data modify storage nonios:shop ui.msg set value {type:"minecraft:plain_message",width:300,contents:{text:"✔ $(name) ($(ptxt)).",color:"green"}}
