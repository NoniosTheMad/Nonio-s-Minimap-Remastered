scoreboard players enable @a demo.fx
execute as @a[scores={demo.fx=1}] run posteffect add @s minecraft:invert
execute as @a[scores={demo.fx=2}] run posteffect add @s minecraft:creeper
execute as @a[scores={demo.fx=3}] run posteffect add @s minecraft:spider
execute as @a[scores={demo.fx=4}] run posteffect add @s minecraft:blur
execute as @a[scores={demo.fx=5}] run posteffect add @s minecraft:entity_outline
execute as @a[scores={demo.fx=6}] run posteffect list @s
execute as @a[scores={demo.fx=7}] run posteffect clear @s
scoreboard players reset @a demo.fx
