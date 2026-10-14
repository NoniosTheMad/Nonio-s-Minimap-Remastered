# Barrier down for good: remove the shield so the obsidian can be mined.
$bossbar set nonios:barrier_$(team) value 0
$function nonios:nexus/fx/shatter with storage nonios:nexus team.$(team)
$title @a[team=$(team)] title {"text":"BARRIER DOWN","color":"dark_red","bold":true}
$title @a[team=$(team)] subtitle {"text":"Defend the obsidian!","color":"red"}
$tellraw @a [{"text":"☠ The $(team) Barrier has fallen!","color":"gold"}]
playsound minecraft:entity.wither.break_block master @a ~ ~ ~ 2 0.7
particle minecraft:explosion_emitter ~ ~0.5 ~
function nonios:nexus/hit_end
kill @s
