# as/at a player with the Monster look
# heartbeat: the shader's thump is at phase 0.10 of a 20-tick period = game tick 2 (mod 20); sent 1 tick early for latency
execute store result score #gt demo.st run time query gametime
scoreboard players operation #gt demo.st %= #20 demo.st
execute if score #gt demo.st matches 1 run playsound nonios:monster.heartbeat player @s ~ ~ ~ 1 1
# madness tier from HP %: >60 none, <=60 1, <=35 2, <=15 3
execute store result score @s demo.mpct run data get entity @s Health 100
execute store result score @s demo.max run attribute @s minecraft:max_health get
execute if score @s demo.max matches 1.. run scoreboard players operation @s demo.mpct /= @s demo.max
scoreboard players set @s demo.mad 0
execute if score @s demo.mpct matches ..60 run scoreboard players set @s demo.mad 1
execute if score @s demo.mpct matches ..35 run scoreboard players set @s demo.mad 2
execute if score @s demo.mpct matches ..15 run scoreboard players set @s demo.mad 3
execute unless score @s demo.mad = @s demo.madp run function demo:monster/changed
# whispers / drone (one roll per tick, #r 1..1000, shared): about every 16 s / 8 s / 4 s
execute if score @s demo.mad matches 1 if score #r demo.st matches 1..3 run function demo:monster/whisper
execute if score @s demo.mad matches 2 if score #r demo.st matches 1..6 run function demo:monster/whisper
execute if score @s demo.mad matches 3 if score #r demo.st matches 1..12 run function demo:monster/whisper
execute if score @s demo.mad matches 3 if score #r demo.st matches 500..502 run playsound nonios:monster.drone ambient @s ~ ~ ~ 0.8 1
