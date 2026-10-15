# dialog demo:events -> trigger demo.ev: 1..8 fire config.events[N-1] at once, 9 random (announced), 10 clear
execute as @a[scores={demo.ev=1..8},limit=1] run function demo:events_fire
execute if data storage demo:arena ev.i run function nonios:arena/event/now with storage demo:arena ev
data remove storage demo:arena ev.i
execute if entity @a[scores={demo.ev=9}] run function nonios:arena/event/random
execute if entity @a[scores={demo.ev=10}] run function demo:events_clear
scoreboard players reset @a[scores={demo.ev=0..}] demo.ev
scoreboard players enable @a demo.ev
