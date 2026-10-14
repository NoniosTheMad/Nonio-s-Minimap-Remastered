# as/at the player, before a class item goes into slot $(slot): whatever was there goes back to the player
# (dropped at its feet with no pickup delay, so it lands in the inventory if there is room). Old class items just vanish.
$execute unless items entity @s $(slot) * run return 0
$execute if items entity @s $(slot) *[minecraft:custom_data~{nx_cls_item:true}] run return run item replace entity @s $(slot) with minecraft:air
summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["nx.cls_stash"]}
$item replace entity @e[type=item,tag=nx.cls_stash,limit=1] contents from entity @s $(slot)
tag @e[type=item,tag=nx.cls_stash] remove nx.cls_stash
$item replace entity @s $(slot) with minecraft:air
