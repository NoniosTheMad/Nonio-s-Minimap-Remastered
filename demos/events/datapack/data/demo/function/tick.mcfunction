execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.ev=1}] at @s run function demo:battle
execute as @a[scores={demo.ev=2}] at @s run function nonios:game/stop
execute as @a[scores={demo.ev=3}] at @s run function demo:ann {i:0}
execute as @a[scores={demo.ev=4}] at @s run function demo:now {i:0}
execute as @a[scores={demo.ev=5}] at @s run function demo:ann {i:1}
execute as @a[scores={demo.ev=6}] at @s run function demo:now {i:1}
execute as @a[scores={demo.ev=7}] at @s run function demo:ann {i:2}
execute as @a[scores={demo.ev=8}] at @s run function demo:now {i:2}
execute as @a[scores={demo.ev=9}] at @s run function demo:ann {i:3}
execute as @a[scores={demo.ev=10}] at @s run function demo:now {i:3}
execute as @a[scores={demo.ev=11}] at @s run function demo:ann {i:4}
execute as @a[scores={demo.ev=12}] at @s run function demo:now {i:4}
execute as @a[scores={demo.ev=13}] at @s run function demo:ann {i:5}
execute as @a[scores={demo.ev=14}] at @s run function demo:now {i:5}
execute as @a[scores={demo.ev=15}] at @s run function demo:random
execute as @a[scores={demo.ev=16}] run function demo:trolls
execute as @a[scores={demo.ev=17}] run function demo:short
execute as @a[scores={demo.ev=18}] run function demo:fast
execute as @a[scores={demo.ev=19}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.ev=20}] at @s run function demo:dummy
execute as @a[scores={demo.ev=21}] run function demo:switch
execute as @a[scores={demo.ev=22}] run function nonios:arena/status
scoreboard players reset @a[scores={demo.ev=1..}] demo.ev
scoreboard players enable @a demo.ev
