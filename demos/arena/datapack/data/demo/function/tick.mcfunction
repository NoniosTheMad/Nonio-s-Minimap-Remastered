execute as @a[tag=!demo.init] run function demo:init
# G menu (dialog demo:arena) -> trigger demo.arena
execute as @a[scores={demo.arena=1}] run function demo:switch_team
execute as @a[scores={demo.arena=2}] at @s run function demo:dummy
execute if entity @a[scores={demo.arena=3}] run kill @e[tag=demo.dummy]
execute if entity @a[scores={demo.arena=3}] run function demo:say {m:"Dummies removed"}
execute if entity @a[scores={demo.arena=4}] run function nonios:arena/event/random
execute if entity @a[scores={demo.arena=5}] run function nonios:arena/event/start {i:0}
execute if entity @a[scores={demo.arena=6}] run function nonios:arena/event/start {i:1}
execute if entity @a[scores={demo.arena=7}] run function nonios:arena/event/now {i:2}
execute if entity @a[scores={demo.arena=8}] run function nonios:arena/lightning/toggle
execute if entity @a[scores={demo.arena=9}] run function demo:speed
execute as @a[scores={demo.arena=10}] at @s run function demo:thief
execute as @a[scores={demo.arena=11}] run function nonios:arena/status
execute if entity @a[scores={demo.arena=12}] run function demo:reset
scoreboard players reset @a[scores={demo.arena=1..}] demo.arena
scoreboard players enable @a demo.arena
