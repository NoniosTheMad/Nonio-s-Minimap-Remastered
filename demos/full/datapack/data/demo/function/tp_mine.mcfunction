# macro {what}: tp next to my team's dream pad / generator
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
$execute if entity @s[team=white] run function demo:tp_at with storage nonios:map white.$(what)
$execute if entity @s[team=black] run function demo:tp_at with storage nonios:map black.$(what)
