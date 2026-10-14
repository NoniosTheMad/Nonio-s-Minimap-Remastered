execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.ec=1}] at @s run function demo:start
execute as @a[scores={demo.ec=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.ec=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.ec=4}] at @s run function demo:switch
execute as @a[scores={demo.ec=5}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.ec=6}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.ec=7}] run function demo:goto_mine
execute as @a[scores={demo.ec=8}] run function demo:goto_enemy
execute as @a[scores={demo.ec=9}] at @s run function nonios:economy/kill/dummy
execute as @a[scores={demo.ec=10}] run function demo:profile
execute as @a[scores={demo.ec=11}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.ec=12}] run function demo:interest
execute as @a[scores={demo.ec=13}] run kill @s
execute as @a[scores={demo.ec=14}] run function nonios:admin/economy/open
execute as @a[scores={demo.ec=15}] run function demo:gear
scoreboard players reset @a[scores={demo.ec=1..}] demo.ec
scoreboard players enable @a demo.ec
