execute as @a[scores={demo.fx=1..4}] run posteffect clear @s
execute as @a[scores={demo.fx=1}] run posteffect add @s nonios:reaper
execute as @a[scores={demo.fx=2}] run posteffect add @s nonios:acid
execute as @a[scores={demo.fx=3}] run posteffect add @s nonios:reaper_luma
execute as @a[scores={demo.fx=4}] run posteffect add @s nonios:reaper
execute as @a[scores={demo.fx=4}] run posteffect add @s nonios:acid
execute as @a[scores={demo.fx=6}] run posteffect list @s
execute as @a[scores={demo.fx=7}] run posteffect clear @s
scoreboard players reset @a demo.fx
scoreboard players enable @a demo.fx
