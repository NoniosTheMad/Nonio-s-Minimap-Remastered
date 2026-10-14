# as/at a player with the Monster look
# heartbeat: the shader's thump is at phase 0.10 of a 20-tick period = game tick 2 (mod 20); sent 1 tick early for latency
execute store result score #gt demo.st run time query gametime
scoreboard players operation #gt demo.st %= #20 demo.st
execute if score #gt demo.st matches 1 run playsound nonios:monster.heartbeat player @s ~ ~ ~ 1 1
# taking damage: an extra hard thump right away (at most once per 10 ticks)
scoreboard players remove @s[scores={demo.dcd=1..}] demo.dcd 1
execute if score @s demo.dmg matches 1.. unless score @s demo.dcd matches 1.. run playsound nonios:monster.heartbeat player @s ~ ~ ~ 1.6 1.2
execute if score @s demo.dmg matches 1.. unless score @s demo.dcd matches 1.. run scoreboard players set @s demo.dcd 10
scoreboard players reset @s demo.dmg
# madness target 0..10 from HP %: starts below 70 %, full at 15 %
execute store result score @s demo.mpct run data get entity @s Health 100
execute store result score @s demo.max run attribute @s minecraft:max_health get
execute if score @s demo.max matches 1.. run scoreboard players operation @s demo.mpct /= @s demo.max
scoreboard players set @s demo.mtg 75
scoreboard players operation @s demo.mtg -= @s demo.mpct
scoreboard players operation @s demo.mtg /= #6 demo.st
execute if score @s demo.mtg matches ..-1 run scoreboard players set @s demo.mtg 0
execute if score @s demo.mtg matches 11.. run scoreboard players set @s demo.mtg 10
# ease the level toward the target: one step every 4 ticks closing in, every 8 ticks letting go
execute unless score @s demo.mad matches 0.. run scoreboard players set @s demo.mad 0
scoreboard players add @s demo.mtk 1
execute if score @s demo.mad = @s demo.mtg run scoreboard players set @s demo.mtk 0
execute if score @s demo.mad < @s demo.mtg if score @s demo.mtk matches 4.. store success score @s demo.mtk run scoreboard players add @s demo.mad 1
execute if score @s demo.mad > @s demo.mtg if score @s demo.mtk matches 8.. store success score @s demo.mtk run scoreboard players remove @s demo.mad 1
execute unless score @s demo.mad = @s demo.madp run function demo:monster/changed
# whispers / drone (one roll per tick, #r 1..1000, shared): about every 16 s / 8 s / 4 s
execute if score @s demo.mad matches 2..4 if score #r demo.st matches 1..3 run function demo:monster/whisper
execute if score @s demo.mad matches 5..7 if score #r demo.st matches 1..6 run function demo:monster/whisper
execute if score @s demo.mad matches 8.. if score #r demo.st matches 1..12 run function demo:monster/whisper
execute if score @s demo.mad matches 8.. if score #r demo.st matches 500..502 run playsound nonios:monster.drone ambient @s ~ ~ ~ 0.8 1
