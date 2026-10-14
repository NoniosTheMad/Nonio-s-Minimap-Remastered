# coin bag worth #drop nx.purse, here. PickupDelay 32767 = vanilla never picks it up or merges it; bag/tick hands it out.
summon minecraft:item ~ ~0.3 ~ {Tags:["nx.coinbag","nx.coinbag_new"],PickupDelay:32767s,CustomNameVisible:1b,Motion:[0.0d,0.25d,0.0d],Item:{id:"minecraft:gold_nugget",count:1,components:{"minecraft:custom_data":{nx_coinbag:1b},"minecraft:enchantment_glint_override":true}}}
execute as @e[type=item,tag=nx.coinbag_new] run function nonios:purse/bag/init
