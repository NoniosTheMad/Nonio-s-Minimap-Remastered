# Class framework tick (from nonios:tick). Near-free when nobody has a class.
execute as @a[scores={nx.cls_left=1..}] run function nonios:class/rejoin
execute as @e[type=player,scores={nx.cls_restock=1..}] at @s run function nonios:class/restock
function nonios:class/gen/tick
# Cracy Frog tongue victims (any class): fall damage on landing, then 3 s of immunity
execute as @e[type=player,tag=nx.frog_yanked] at @s run function nonios:class/cracy_frog/yanked_tick
execute as @e[type=player,tag=nx.frog_immune] run function nonios:class/cracy_frog/immune_tick
# Cracy Frog brooms nobody rides
execute as @e[type=happy_ghast,tag=nx.frog_mount] unless predicate {type:"minecraft:entity_properties",entity:"this",predicate:{"minecraft:passenger":{"minecraft:entity_type":"minecraft:player"}}} run function nonios:class/cracy_frog/mount_orphan
# Reaper lantern: bound victims (any class)
execute as @e[tag=nx.reaper_bound] at @s run function nonios:class/reaper/bound_tick
# Balrog trails outlive their Balrog (4.5 s)
execute as @e[type=marker,tag=nx.bal_trail] at @s run function nonios:class/balrog/trail
execute as @a[scores={nx.cls_ask=1..}] at @s run function nonios:class/cracy_frog/ask
scoreboard players add #t nx.cls_tmp 1
execute if score #t nx.cls_tmp matches 20.. run function nonios:class/second
scoreboard players enable @a nx.cls_ask
