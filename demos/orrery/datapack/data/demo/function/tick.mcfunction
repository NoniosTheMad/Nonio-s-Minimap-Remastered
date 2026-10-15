execute as @a[scores={demo.or=1}] run tp @s 0 52 92 180 -10
execute as @a[scores={demo.or=2}] run tp @s 0 50 -92 0 -10
execute as @a[scores={demo.or=3}] run tp @s -6 57 62 180 -30
execute as @a[scores={demo.or=4}] run tp @s 0 129 39 180 -20
execute as @a[scores={demo.or=5}] run tp @s -16 129 17 243 -5
execute as @a[scores={demo.or=6}] run tp @s 0 171 16 0 0
execute as @a[scores={demo.or=7}] run tp @s 0 213 -4 0 0
execute as @a[scores={demo.or=8}] run tp @s 0 88 12 180 0
execute as @a[scores={demo.or=9}] run tp @s 0 37 -4 180 0
execute as @a[scores={demo.or=10}] run tp @s -37 64 -37 135 -10
execute as @a[scores={demo.or=11}] run tp @s 74 63 -36 64 -5
execute if entity @a[scores={demo.or=12}] run time set 6000
execute if entity @a[scores={demo.or=13}] run time set 18000
execute as @a[scores={demo.or=14}] run gamemode creative @s
execute as @a[scores={demo.or=15}] run gamemode survival @s
execute as @a[scores={demo.or=16}] run gamemode spectator @s
scoreboard players reset @a[scores={demo.or=1..}] demo.or
scoreboard players enable @a demo.or
