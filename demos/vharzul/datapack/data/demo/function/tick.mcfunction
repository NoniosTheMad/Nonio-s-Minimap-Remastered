execute as @a[scores={demo.vz=1}] run tp @s 0 48 129 180 -8
execute as @a[scores={demo.vz=2}] run tp @s 0 48 102 180 -10
execute as @a[scores={demo.vz=3}] run tp @s 0 76 49 180 0
execute as @a[scores={demo.vz=4}] run tp @s -3 89 15 0 0
execute as @a[scores={demo.vz=5}] run tp @s 0 89 6 180 -20
execute as @a[scores={demo.vz=6}] run tp @s 0 180 4 180 0
execute as @a[scores={demo.vz=7}] run tp @s -16 89 -5 -136 0
execute as @a[scores={demo.vz=8}] run tp @s 0 80 26 180 0
execute as @a[scores={demo.vz=9}] run tp @s 80 54 -53 56 -15
execute as @a[scores={demo.vz=10}] run tp @s -90 63 12 -109 -10
execute as @a[scores={demo.vz=11}] run time set 6000
execute as @a[scores={demo.vz=12}] run time set 18000
execute as @a[scores={demo.vz=13}] run gamemode creative @s
execute as @a[scores={demo.vz=14}] run gamemode survival @s
scoreboard players reset @a[scores={demo.vz=1..}] demo.vz
scoreboard players enable @a demo.vz
