# Once a second: shop-class kits stay complete (armour back on, tools back in the inventory), stray class items vanish.
scoreboard players set #t nx.cls_tmp 0
execute as @e[type=player,scores={nx.class=1..}] at @s run function nonios:class/gen/check
execute as @e[type=player] run function nonios:class/gen/purge
function nonios:class/gen/second
# stray Angel halos (their Angel went offline or lost the class)
execute as @e[type=text_display,tag=nx.ang_halo] run function nonios:class/angel/halo_check
