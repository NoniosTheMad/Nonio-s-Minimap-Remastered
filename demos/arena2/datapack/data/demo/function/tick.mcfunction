execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.ar2=1}] at @s run function demo:start
execute as @a[scores={demo.ar2=2}] at @s run function demo:battle
execute as @a[scores={demo.ar2=3}] at @s run function nonios:game/skip
execute as @a[scores={demo.ar2=4}] at @s run function nonios:game/stop
execute as @a[scores={demo.ar2=5}] at @s run function demo:switch
execute as @a[scores={demo.ar2=6}] run function demo:gear
execute as @a[scores={demo.ar2=7}] run function demo:fast
execute as @a[scores={demo.ar2=8}] run function demo:tp_gate
execute as @a[scores={demo.ar2=9}] run function demo:tp_exit
execute as @a[scores={demo.ar2=10}] run function demo:say {m:"Gate slot re-rolled",cmd:"function nonios:arena/gate/rotate"}
execute as @a[scores={demo.ar2=11}] run function nonios:arena/gate/status
execute as @a[scores={demo.ar2=12}] run function demo:tp_core
execute as @a[scores={demo.ar2=13}] run function demo:break_core
execute as @a[scores={demo.ar2=14}] run function demo:sample
execute as @a[scores={demo.ar2=15}] run function nonios:arena/core/status
execute as @a[scores={demo.ar2=16}] run function demo:status
execute as @a[scores={demo.ar2=17}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.ar2=18}] run function nonios:admin
execute as @a[scores={demo.ar2=19}] run function demo:say {m:"Preparation time = 20 s (next Start)",cmd:"data modify storage nonios:config prep_time set value 20"}
execute as @a[scores={demo.ar2=20}] run function nonios:game/tp_arena with storage nonios:map arena
scoreboard players reset @a[scores={demo.ar2=1..}] demo.ar2
scoreboard players enable @a demo.ar2
