# Balrog (V2 secret 10000-coin kit): everyone hears it wake
tag @s add nx.cls_balrog
function nonios:class/fill_hp
effect give @s minecraft:fire_resistance infinite 0 true
particle minecraft:flame ~ ~1.5 ~ 0.8 1.2 0.8 0.05 80
particle minecraft:large_smoke ~ ~1.5 ~ 0.8 1.2 0.8 0.02 60
execute as @a at @s run playsound minecraft:entity.wither.spawn master @s ~ ~ ~ 0.6 0.5
tellraw @a [{"text":"☠ ","color":"dark_red"},{"text":"A Balrog has awoken.","color":"gold","italic":true}]
