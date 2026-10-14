execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.m5=1}] at @s run function demo:start
execute as @a[scores={demo.m5=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.m5=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.m5=4}] at @s run function demo:switch
execute as @a[scores={demo.m5=5}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.m5=6}] at @s run function demo:hostiles
execute as @a[scores={demo.m5=7}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.m5=8}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.m5=9}] at @s run function demo:break_mine
execute as @a[scores={demo.m5=10}] at @s run function demo:break_enemy
execute as @a[scores={demo.m5=11}] run kill @s
execute as @a[scores={demo.m5=12}] run function nonios:admin
execute as @a[scores={demo.m5=13}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.m5=14}] run function demo:gear
execute as @a[scores={demo.m5=15}] run function demo:fast
execute as @a[scores={demo.m5=16}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.m5=17}] run function demo:unlock
execute as @a[scores={demo.m5=18}] run function demo:tp_mine {what:"dream"}
execute as @a[scores={demo.m5=19}] run function demo:tp_mine {what:"gen"}
execute as @a[scores={demo.m5=20}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.m5=21}] at @s run function demo:captor
execute as @a[scores={demo.m5=22}] run function demo:say {m:"Random arena event",cmd:"function nonios:arena/event/random"}
execute as @a[scores={demo.m5=23}] run function demo:say {m:"Lightning toggled",cmd:"function nonios:arena/lightning/toggle"}
execute as @a[scores={demo.m5=24}] at @s run function demo:gen_drop
execute as @a[scores={demo.m5=25}] run function nonios:dream/force_exit
execute as @a[scores={demo.m5=26}] run function demo:status_ask
execute as @a[scores={demo.m5=27}] at @s run function nonios:class/set_id {id:"reaper"}
execute as @a[scores={demo.m5=28}] at @s run function nonios:class/set_id {id:"cracy_frog"}
execute as @a[scores={demo.m5=29}] at @s run function nonios:class/set_id {id:"warrior"}
execute as @a[scores={demo.m5=30}] run function nonios:class/remove
execute as @a[scores={demo.m5=31}] at @s run function demo:level_up
execute as @a[scores={demo.m5=32}] at @s run function demo:shop_anywhere
execute as @a[scores={demo.m5=33}] run function demo:tp_mine {what:"shop"}
execute as @a[scores={demo.m5=34}] run function demo:class_status
scoreboard players reset @a[scores={demo.m5=1..}] demo.m5
scoreboard players enable @a demo.m5
