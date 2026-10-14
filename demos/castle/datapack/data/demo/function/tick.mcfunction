execute as @a[scores={demo.cs=1}] run tp @s 0 54 44 180 -5
execute as @a[scores={demo.cs=2}] run tp @s -1 54 -19 180 0
execute as @a[scores={demo.cs=3}] run tp @s -3 62 -20 160 0
execute as @a[scores={demo.cs=4}] run tp @s 6 70 -25 90 0
execute as @a[scores={demo.cs=5}] run tp @s 0 46 -20 180 0
execute as @a[scores={demo.cs=6}] run tp @s 31 64 0 90 0
execute as @a[scores={demo.cs=7}] run tp @s -12 78 -18 0 10
execute as @a[scores={demo.cs=8}] run gamemode creative @s
execute as @a[scores={demo.cs=9}] run gamemode survival @s
execute as @a[scores={demo.cs=10}] run gamemode spectator @s
scoreboard players reset @a[scores={demo.cs=1..}] demo.cs
scoreboard players enable @a demo.cs
