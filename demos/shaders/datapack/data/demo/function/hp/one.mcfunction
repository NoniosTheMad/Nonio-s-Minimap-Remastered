# health -> team colour (= what the thermal shader reads). Tiers above 20 hearts double: log2 scale.
execute store result score @s demo.hp run data get entity @s Health
execute store result score @s demo.abs run data get entity @s AbsorptionAmount
execute store result score @s demo.max run attribute @s minecraft:max_health get
scoreboard players operation @s demo.tot = @s demo.hp
scoreboard players operation @s demo.tot += @s demo.abs
scoreboard players operation @s demo.pct = @s demo.hp
scoreboard players operation @s demo.pct *= #100 demo.st
execute if score @s demo.max matches 1.. run scoreboard players operation @s demo.pct /= @s demo.max
execute if score @s demo.tot matches 81.. run team join demo.hp5 @s
execute if score @s demo.tot matches 41..80 run team join demo.hp4 @s
execute if score @s demo.tot matches ..40 if score @s demo.pct matches 66.. run team join demo.hp3 @s
execute if score @s demo.tot matches ..40 if score @s demo.pct matches 31..65 run team join demo.hp2 @s
execute if score @s demo.tot matches ..40 if score @s demo.pct matches ..30 run team join demo.hp1 @s
effect give @s glowing infinite 0 true
