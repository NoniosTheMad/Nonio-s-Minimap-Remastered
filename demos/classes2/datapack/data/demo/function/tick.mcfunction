execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.c2=1}] at @s run function demo:start
execute as @a[scores={demo.c2=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.c2=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.c2=4}] at @s run function demo:switch
execute as @a[scores={demo.c2=5}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.c2=6}] at @s run function demo:hostiles
execute as @a[scores={demo.c2=7}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.c2=8}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.c2=9}] at @s run function demo:break_mine
execute as @a[scores={demo.c2=10}] at @s run function demo:break_enemy
execute as @a[scores={demo.c2=11}] run kill @s
execute as @a[scores={demo.c2=12}] run function nonios:admin
execute as @a[scores={demo.c2=13}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.c2=14}] run function demo:gear
execute as @a[scores={demo.c2=15}] run function demo:fast
execute as @a[scores={demo.c2=16}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.c2=17}] run function demo:unlock
execute as @a[scores={demo.c2=18}] run function demo:tp_mine {what:"dream"}
execute as @a[scores={demo.c2=19}] run function demo:tp_mine {what:"gen"}
execute as @a[scores={demo.c2=20}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.c2=21}] at @s run function demo:captor
execute as @a[scores={demo.c2=22}] run function demo:say {m:"Random arena event",cmd:"function nonios:arena/event/random"}
execute as @a[scores={demo.c2=23}] run function demo:say {m:"Lightning toggled",cmd:"function nonios:arena/lightning/toggle"}
execute as @a[scores={demo.c2=24}] at @s run function demo:gen_drop
execute as @a[scores={demo.c2=25}] run function nonios:dream/force_exit
execute as @a[scores={demo.c2=26}] run function demo:status_ask
execute as @a[scores={demo.c2=27}] at @s run function nonios:class/set_id {id:"reaper"}
execute as @a[scores={demo.c2=28}] at @s run function nonios:class/set_id {id:"cracy_frog"}
execute as @a[scores={demo.c2=29}] at @s run function nonios:class/set_id {id:"warrior"}
execute as @a[scores={demo.c2=30}] run function nonios:class/remove
execute as @a[scores={demo.c2=31}] at @s run function demo:level_up
execute as @a[scores={demo.c2=32}] at @s run function demo:shop_anywhere
execute as @a[scores={demo.c2=33}] run function demo:tp_mine {what:"shop"}
execute as @a[scores={demo.c2=34}] run function demo:class_status
execute as @a[scores={demo.c2=35}] at @s run function nonios:class/set_id {id:"archer"}
execute as @a[scores={demo.c2=36}] at @s run function nonios:class/set_id {id:"miner"}
execute as @a[scores={demo.c2=37}] at @s run function nonios:class/set_id {id:"tank"}
execute as @a[scores={demo.c2=38}] at @s run function nonios:class/set_id {id:"ninja"}
execute as @a[scores={demo.c2=39}] at @s run function nonios:class/set_id {id:"berserker"}
execute as @a[scores={demo.c2=40}] at @s run function nonios:class/set_id {id:"monster"}
execute as @a[scores={demo.c2=41}] at @s run function nonios:class/set_id {id:"balrog"}
execute as @a[scores={demo.c2=42}] at @s run function demo:targets
execute as @a[scores={demo.c2=43}] at @s run function demo:wave
execute as @a[scores={demo.c2=44}] run function demo:reset_cd
execute as @a[scores={demo.c2=45}] run function demo:clear_mobs
scoreboard players reset @a[scores={demo.c2=1..}] demo.c2
scoreboard players enable @a demo.c2
