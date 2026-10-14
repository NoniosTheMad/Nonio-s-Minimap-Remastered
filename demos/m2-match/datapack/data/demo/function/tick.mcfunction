execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.m2=1}] at @s run function demo:start
execute as @a[scores={demo.m2=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.m2=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.m2=4}] at @s run function demo:switch
execute as @a[scores={demo.m2=5}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.m2=6}] at @s run function demo:hostiles
execute as @a[scores={demo.m2=7}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.m2=8}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.m2=9}] at @s run function demo:break_mine
execute as @a[scores={demo.m2=10}] at @s run function demo:break_enemy
execute as @a[scores={demo.m2=11}] run kill @s
execute as @a[scores={demo.m2=12}] run function nonios:admin
execute as @a[scores={demo.m2=13}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.m2=14}] run function demo:gear
scoreboard players reset @a[scores={demo.m2=1..}] demo.m2
scoreboard players enable @a demo.m2
