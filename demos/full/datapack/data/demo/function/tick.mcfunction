execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.full=1}] at @s run function demo:start
execute as @a[scores={demo.full=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.full=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.full=4}] at @s run function demo:switch
execute as @a[scores={demo.full=5}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.full=6}] at @s run function demo:hostiles
execute as @a[scores={demo.full=7}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.full=8}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.full=9}] at @s run function demo:break_mine
execute as @a[scores={demo.full=10}] at @s run function demo:break_enemy
execute as @a[scores={demo.full=11}] run kill @s
execute as @a[scores={demo.full=12}] run function nonios:admin
execute as @a[scores={demo.full=13}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.full=14}] run function demo:gear
execute as @a[scores={demo.full=15}] run function demo:fast
execute as @a[scores={demo.full=16}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.full=17}] run function demo:unlock
execute as @a[scores={demo.full=18}] run function demo:tp_mine {what:"dream"}
execute as @a[scores={demo.full=19}] run function demo:tp_mine {what:"gen"}
execute as @a[scores={demo.full=20}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.full=21}] at @s run function demo:captor
execute as @a[scores={demo.full=22}] run function demo:say {m:"Random arena event",cmd:"function nonios:arena/event/random"}
execute as @a[scores={demo.full=23}] run function demo:say {m:"Lightning toggled",cmd:"function nonios:arena/lightning/toggle"}
execute as @a[scores={demo.full=24}] at @s run function demo:gen_drop
execute as @a[scores={demo.full=25}] run function nonios:dream/force_exit
execute as @a[scores={demo.full=26}] run function demo:status_ask
execute as @a[scores={demo.full=27}] at @s run function nonios:class/set_id {id:"reaper"}
execute as @a[scores={demo.full=28}] at @s run function nonios:class/set_id {id:"cracy_frog"}
execute as @a[scores={demo.full=29}] at @s run function nonios:class/set_id {id:"warrior"}
execute as @a[scores={demo.full=30}] run function nonios:class/remove
execute as @a[scores={demo.full=31}] at @s run function demo:level_up
execute as @a[scores={demo.full=32}] at @s run function demo:shop_anywhere
execute as @a[scores={demo.full=33}] run function demo:tp_mine {what:"shop"}
execute as @a[scores={demo.full=34}] run function demo:class_status
execute as @a[scores={demo.full=35}] at @s run function nonios:class/set_id {id:"archer"}
execute as @a[scores={demo.full=36}] at @s run function nonios:class/set_id {id:"miner"}
execute as @a[scores={demo.full=37}] at @s run function nonios:class/set_id {id:"tank"}
execute as @a[scores={demo.full=38}] at @s run function nonios:class/set_id {id:"ninja"}
execute as @a[scores={demo.full=39}] at @s run function nonios:class/set_id {id:"berserker"}
execute as @a[scores={demo.full=40}] at @s run function nonios:class/set_id {id:"monster"}
execute as @a[scores={demo.full=41}] at @s run function nonios:class/set_id {id:"balrog"}
execute as @a[scores={demo.full=42}] at @s run function demo:targets
execute as @a[scores={demo.full=43}] at @s run function demo:wave
execute as @a[scores={demo.full=44}] run function demo:reset_cd
execute as @a[scores={demo.full=45}] run function demo:clear_mobs
execute as @a[scores={demo.full=46}] run function demo:tp_gate
execute as @a[scores={demo.full=47}] run function demo:tp_exit
execute as @a[scores={demo.full=48}] run function demo:say {m:"Gate slot re-rolled",cmd:"function nonios:arena/gate/rotate"}
execute as @a[scores={demo.full=49}] run function nonios:arena/gate/status
execute as @a[scores={demo.full=50}] run function demo:tp_core
execute as @a[scores={demo.full=51}] run function demo:break_core
execute as @a[scores={demo.full=52}] run function nonios:arena/core/status
execute as @a[scores={demo.full=53}] run function demo:say {m:"+10000 coins",cmd:"scoreboard players add @s nx.coins 10000"}
execute as @a[scores={demo.full=54}] at @s run function demo:shop_open
execute as @a[scores={demo.full=55}] run function demo:say {m:"Inventory cleared",cmd:"clear @s"}
execute as @a[scores={demo.full=56}] run function demo:offering
execute as @a[scores={demo.full=57}] run function demo:say {m:"8 iron, 8 gold, 2 diamond blocks",cmd:"function demo:offering_some"}
execute as @a[scores={demo.full=58}] run function demo:tp_altar
execute as @a[scores={demo.full=59}] run function demo:tp_enemy_spawn
execute as @a[scores={demo.full=60}] run function demo:say {m:"Emerald Talisman: right-click it to wear it",cmd:"function nonios:talisman/give"}
execute as @a[scores={demo.full=61}] run function nonios:special/dragon_skull
execute as @a[scores={demo.full=62}] run function demo:team_status
execute as @a[scores={demo.full=63}] run function demo:guard_toggle
execute as @a[scores={demo.full=64}] run function demo:say {m:"+3,200,000 coins",cmd:"scoreboard players add @s nx.coins 3200000"}
scoreboard players reset @a[scores={demo.full=1..}] demo.full
scoreboard players enable @a demo.full
