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
execute as @a[scores={demo.ec=16}] at @s run function demo:ores
execute as @a[scores={demo.ec=17}] run function demo:clock
execute as @a[scores={demo.ec=18}] run function demo:status
execute as @a[scores={demo.ec=19}] run function demo:altar
execute as @a[scores={demo.ec=20}] run function demo:im/open
execute as @a[scores={demo.ec=21}] run function demo:im/mode {m:1}
execute as @a[scores={demo.ec=22}] run function demo:im/mode {m:2}
execute as @a[scores={demo.ec=23}] run function demo:im/mode {m:3}
execute as @a[scores={demo.ec=24}] run function demo:im/clock {t:0}
execute as @a[scores={demo.ec=25}] run function demo:im/clock {t:12000}
execute as @a[scores={demo.ec=26}] run function demo:im/clock {t:24000}
execute as @a[scores={demo.ec=27}] run function demo:im/clock {t:36000}
execute as @a[scores={demo.ec=28}] run function demo:im/bank {n:500}
execute as @a[scores={demo.ec=29}] run function demo:im/bank {n:2000}
execute as @a[scores={demo.ec=30}] run function demo:im/bank {n:10000}
execute as @a[scores={demo.ec=31}] run function demo:im/pay
execute as @a[scores={demo.ec=32}] run dialog show @s demo:economy
scoreboard players reset @a[scores={demo.ec=1..}] demo.ec
scoreboard players enable @a demo.ec
