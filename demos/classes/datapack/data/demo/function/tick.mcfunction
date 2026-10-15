execute as @a[tag=!demo.init] run function demo:init
# real deaths: the demo plays M2's part and calls the class hooks once the player has respawned
execute as @e[type=player,scores={demo.died=1..}] at @s run function demo:respawned
# G menu (demo:classes dialog) -> trigger demo.cls
execute as @a[scores={demo.cls=1}] at @s run function nonios:class/set_id {id:"reaper"}
execute as @a[scores={demo.cls=2}] run function nonios:class/cracy_frog/ask_step {step:1}
execute as @a[scores={demo.cls=3}] at @s run function nonios:class/set_id {id:"cracy_frog"}
execute as @a[scores={demo.cls=4}] at @s run function nonios:class/set_id {id:"warrior"}
execute as @a[scores={demo.cls=13}] at @s run function nonios:class/set_id {id:"champion"}
execute as @a[scores={demo.cls=14}] at @s run function nonios:class/set_id {id:"archer"}
execute as @a[scores={demo.cls=15}] at @s run function nonios:class/set_id {id:"miner"}
execute as @a[scores={demo.cls=16}] at @s run function nonios:class/set_id {id:"tank"}
execute as @a[scores={demo.cls=17}] at @s run function nonios:class/set_id {id:"ninja"}
execute as @a[scores={demo.cls=18}] at @s run function nonios:class/set_id {id:"berserker"}
execute as @a[scores={demo.cls=19}] at @s run function nonios:class/set_id {id:"monster"}
execute as @a[scores={demo.cls=20}] at @s run function nonios:class/set_id {id:"balrog"}
execute as @a[scores={demo.cls=5}] at @s run function demo:level_up
execute as @a[scores={demo.cls=6}] run function nonios:class/remove
execute as @a[scores={demo.cls=7}] at @s run function demo:sim_death
execute as @a[scores={demo.cls=8}] run kill @s
execute as @a[scores={demo.cls=9}] at @s run function demo:dummies
execute as @a[scores={demo.cls=10}] at @s run function demo:reset_cd
execute as @a[scores={demo.cls=11}] run function demo:gamemode
execute as @a[scores={demo.cls=12}] run function demo:status
scoreboard players reset @a[scores={demo.cls=1..}] demo.cls
scoreboard players enable @a demo.cls
