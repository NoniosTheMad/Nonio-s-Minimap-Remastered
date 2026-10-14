execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.ar3=1}] at @s run function demo:battle
execute as @a[scores={demo.ar3=2}] at @s run function demo:start
execute as @a[scores={demo.ar3=3}] at @s run function nonios:game/skip
execute as @a[scores={demo.ar3=4}] at @s run function nonios:game/stop
execute as @a[scores={demo.ar3=5}] at @s run function demo:switch
execute as @a[scores={demo.ar3=6}] run function demo:gear
execute as @a[scores={demo.ar3=7}] run function demo:fast
execute as @a[scores={demo.ar3=8}] run function demo:tp_gen
execute as @a[scores={demo.ar3=9}] at @s run function demo:grow
execute as @a[scores={demo.ar3=10}] at @s run function demo:gen_up
execute as @a[scores={demo.ar3=11}] run function demo:lucky
execute as @a[scores={demo.ar3=12}] run function demo:tp_cgen
execute as @a[scores={demo.ar3=13}] run function demo:bank {n:1000}
execute as @a[scores={demo.ar3=14}] run function demo:bank0
execute as @a[scores={demo.ar3=15}] run function demo:say {m:"Centre generator: drop now",cmd:"scoreboard players set @e[type=marker,tag=nx.cgen] nx.gen_t 1"}
execute as @a[scores={demo.ar3=16}] run function nonios:game/tp_arena with storage nonios:map arena
execute as @a[scores={demo.ar3=17}] run function demo:own_nodes
execute as @a[scores={demo.ar3=18}] run function demo:prot
execute as @a[scores={demo.ar3=19}] run function demo:say {m:"Random event announced",cmd:"function nonios:arena/event/random"}
execute as @a[scores={demo.ar3=20}] run function demo:status
execute as @a[scores={demo.ar3=21}] at @s run function nonios:admin/rebuild
execute as @a[scores={demo.ar3=22}] run function nonios:admin
scoreboard players reset @a[scores={demo.ar3=1..}] demo.ar3
scoreboard players enable @a demo.ar3
