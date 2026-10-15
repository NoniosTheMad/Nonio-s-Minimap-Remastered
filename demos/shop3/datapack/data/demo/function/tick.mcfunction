execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.shop3=1}] at @s run function demo:start
execute as @a[scores={demo.shop3=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.shop3=3}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.shop3=4}] run function demo:say {m:"+100000 coins",cmd:"scoreboard players add @s nx.coins 100000"}
execute as @a[scores={demo.shop3=5}] at @s run function demo:shop_anywhere
execute as @a[scores={demo.shop3=6}] run function demo:say {m:"Inventory cleared",cmd:"clear @s"}
execute as @a[scores={demo.shop3=7}] run function demo:fill
execute as @a[scores={demo.shop3=8}] run function demo:gear
execute as @a[scores={demo.shop3=9}] run function demo:say {m:"Starting kit",cmd:"function #nonios:kit/start"}
execute as @a[scores={demo.shop3=10}] run function demo:bow
execute as @a[scores={demo.shop3=11}] run function demo:tp_nexus
execute as @a[scores={demo.shop3=12}] run function demo:nexus_hp
execute as @a[scores={demo.shop3=13}] run function demo:catalog {f:"demo:catalog_stress",m:"stress, 452 items"}
execute as @a[scores={demo.shop3=14}] run function demo:catalog {f:"nonios:shop/catalog",m:"real, 90 items"}
execute as @a[scores={demo.shop3=15}] at @s run function demo:switch
execute as @a[scores={demo.shop3=16}] at @s run function nonios:game/stop
scoreboard players reset @a[scores={demo.shop3=1..}] demo.shop3
scoreboard players enable @a demo.shop3
