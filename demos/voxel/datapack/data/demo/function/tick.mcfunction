execute as @a[scores={demo.vx=1}] run tp @s -28 53 6 -90 0
execute as @a[scores={demo.vx=2}] run tp @s 21 52 -17 30 0
execute as @a[scores={demo.vx=3}] run tp @s 10 56 26 174 -10
execute as @a[scores={demo.vx=4}] run tp @s 8 67 4 0 -30
execute as @a[scores={demo.vx=5}] run gamemode creative @s
execute as @a[scores={demo.vx=6}] run gamemode survival @s
execute as @a[scores={demo.vx=7}] run gamemode spectator @s
scoreboard players reset @a[scores={demo.vx=1..}] demo.vx
scoreboard players enable @a demo.vx
