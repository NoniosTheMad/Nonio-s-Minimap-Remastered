execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.team2=1}] at @s run function demo:start
execute as @a[scores={demo.team2=2}] at @s run function nonios:game/skip
execute as @a[scores={demo.team2=3}] at @s run function nonios:game/stop
execute as @a[scores={demo.team2=4}] at @s run function demo:switch
execute as @a[scores={demo.team2=5}] at @s run function demo:dummy {ai:"NoAI:1b,",n:"Dummy"}
execute as @a[scores={demo.team2=6}] at @s run function demo:hostiles
execute as @a[scores={demo.team2=7}] run function demo:say {m:"+100 coins",cmd:"scoreboard players add @s nx.coins 100"}
execute as @a[scores={demo.team2=8}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.team2=9}] at @s run function demo:break_mine
execute as @a[scores={demo.team2=10}] at @s run function demo:break_enemy
execute as @a[scores={demo.team2=11}] run kill @s
execute as @a[scores={demo.team2=12}] run function nonios:admin
execute as @a[scores={demo.team2=13}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.team2=14}] run function demo:gear
execute as @a[scores={demo.team2=15}] run function demo:fast
execute as @a[scores={demo.team2=16}] run function demo:say {m:"+1000 coins",cmd:"scoreboard players add @s nx.coins 1000"}
execute as @a[scores={demo.team2=17}] run function demo:unlock
execute as @a[scores={demo.team2=18}] run function demo:tp_mine {what:"dream"}
execute as @a[scores={demo.team2=19}] run function demo:tp_mine {what:"gen"}
execute as @a[scores={demo.team2=20}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.team2=21}] at @s run function demo:captor
execute as @a[scores={demo.team2=22}] run function demo:say {m:"Random arena event",cmd:"function nonios:arena/event/random"}
execute as @a[scores={demo.team2=23}] run function demo:say {m:"Lightning toggled",cmd:"function nonios:arena/lightning/toggle"}
execute as @a[scores={demo.team2=24}] at @s run function demo:gen_drop
execute as @a[scores={demo.team2=25}] run function nonios:dream/force_exit
execute as @a[scores={demo.team2=26}] run function demo:status_ask
execute as @a[scores={demo.team2=27}] at @s run function nonios:class/set_id {id:"reaper"}
execute as @a[scores={demo.team2=28}] at @s run function nonios:class/set_id {id:"cracy_frog"}
execute as @a[scores={demo.team2=29}] at @s run function nonios:class/set_id {id:"warrior"}
execute as @a[scores={demo.team2=30}] run function nonios:class/remove
execute as @a[scores={demo.team2=31}] at @s run function demo:level_up
execute as @a[scores={demo.team2=32}] at @s run function demo:shop_anywhere
execute as @a[scores={demo.team2=33}] run function demo:tp_mine {what:"shop"}
execute as @a[scores={demo.team2=34}] run function demo:class_status
execute as @a[scores={demo.team2=35}] at @s run function nonios:class/set_id {id:"archer"}
execute as @a[scores={demo.team2=36}] at @s run function nonios:class/set_id {id:"miner"}
execute as @a[scores={demo.team2=37}] at @s run function nonios:class/set_id {id:"tank"}
execute as @a[scores={demo.team2=38}] at @s run function nonios:class/set_id {id:"ninja"}
execute as @a[scores={demo.team2=39}] at @s run function nonios:class/set_id {id:"berserker"}
execute as @a[scores={demo.team2=40}] at @s run function nonios:class/set_id {id:"monster"}
execute as @a[scores={demo.team2=41}] at @s run function nonios:class/set_id {id:"balrog"}
execute as @a[scores={demo.team2=42}] at @s run function demo:targets
execute as @a[scores={demo.team2=43}] at @s run function demo:wave
execute as @a[scores={demo.team2=44}] run function demo:reset_cd
execute as @a[scores={demo.team2=45}] run function demo:clear_mobs
execute as @a[scores={demo.team2=46}] run function demo:tp_gate
execute as @a[scores={demo.team2=47}] run function demo:tp_exit
execute as @a[scores={demo.team2=48}] run function demo:say {m:"Gate slot re-rolled",cmd:"function nonios:arena/gate/rotate"}
execute as @a[scores={demo.team2=49}] run function nonios:arena/gate/status
execute as @a[scores={demo.team2=50}] run function demo:tp_core
execute as @a[scores={demo.team2=51}] run function demo:break_core
execute as @a[scores={demo.team2=52}] run function nonios:arena/core/status
execute as @a[scores={demo.team2=53}] run function demo:offering
execute as @a[scores={demo.team2=54}] run function demo:say {m:"8 iron, 8 gold, 2 diamond blocks",cmd:"function demo:offering_some"}
execute as @a[scores={demo.team2=55}] run function demo:tp_altar
execute as @a[scores={demo.team2=56}] run function demo:tp_enemy_spawn
execute as @a[scores={demo.team2=57}] run function demo:say {m:"Emerald Talisman: right-click it to wear it",cmd:"function nonios:talisman/give"}
execute as @a[scores={demo.team2=58}] run function nonios:special/dragon_skull
execute as @a[scores={demo.team2=59}] run function demo:team_status
execute as @a[scores={demo.team2=60}] run function demo:guard_toggle
execute as @a[scores={demo.team2=61}] run function demo:say {m:"+3,200,000 coins",cmd:"scoreboard players add @s nx.coins 3200000"}
scoreboard players reset @a[scores={demo.team2=1..}] demo.team2
scoreboard players enable @a demo.team2
