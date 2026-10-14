# Class framework tick (from nonios:tick). Near-free when nobody has a class.
execute as @a[scores={nx.cls_left=1..}] run function nonios:class/rejoin
execute as @e[type=player,scores={nx.cls_restock=1..}] at @s run function nonios:class/restock
function nonios:class/gen/tick
execute as @a[scores={nx.cls_ask=1..}] run function nonios:class/cracy_frog/ask
scoreboard players add #t nx.cls_tmp 1
execute if score #t nx.cls_tmp matches 20.. run function nonios:class/second
scoreboard players enable @a nx.cls_ask
