# layers / presets / clear (1..49)
execute as @a[scores={demo.fx=1..49}] run function demo:fx/set
execute as @a[scores={demo.fx=50}] run function demo:fx/status
# time of day
execute if entity @a[scores={demo.fx=60}] run function demo:time {t:23400,name:"Dawn"}
execute if entity @a[scores={demo.fx=61}] run function demo:time {t:6000,name:"Noon"}
execute if entity @a[scores={demo.fx=62}] run function demo:time {t:12600,name:"Dusk"}
execute if entity @a[scores={demo.fx=63}] run function demo:time {t:18000,name:"Midnight"}
execute if entity @a[scores={demo.fx=64}] run function demo:cycle {on:"true",msg:"Day/night cycle on"}
execute if entity @a[scores={demo.fx=65}] run function demo:cycle {on:"false",msg:"Day/night cycle off (time frozen)"}
# gallery
execute as @a[scores={demo.fx=70}] run tp @s 0.5 64 4.5 0 15
execute if entity @a[scores={demo.fx=71}] run function demo:rebuild
# HP test (Thermal / Angel)
execute as @a[scores={demo.fx=80}] run function demo:hp/hurt
execute as @a[scores={demo.fx=81}] run effect give @s instant_health 1 4 true
execute as @a[scores={demo.fx=82}] run effect give @s absorption 600 9 true
execute as @a[scores={demo.fx=83}] run effect give @s absorption 600 19 true
execute as @a[scores={demo.fx=84}] run effect clear @s absorption
# post effects are client-side: re-apply after a rejoin
execute as @a[scores={demo.left=1..}] run function demo:fx/apply
scoreboard players reset @a[scores={demo.left=1..}] demo.left
function demo:hp/update
# Monster look: heartbeat sound + madness tiers
execute if entity @a[scores={demo.look=5}] store result score #r demo.st run random value 1..1000
execute as @a[scores={demo.look=5}] at @s run function demo:monster/tick
scoreboard players add #hud demo.st 1
execute if score #hud demo.st matches 40.. as @a run function demo:fx/hud
execute if score #hud demo.st matches 40.. run scoreboard players set #hud demo.st 0
# reset first, enable last (enable before reset would re-lock the trigger)
scoreboard players reset @a demo.fx
scoreboard players enable @a demo.fx
