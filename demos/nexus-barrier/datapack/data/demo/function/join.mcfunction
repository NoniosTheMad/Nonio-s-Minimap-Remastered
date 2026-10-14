$execute if entity @s[team=$(team)] run return run tellraw @s {"text":"[demo] Already on team $(team).","color":"gray"}
$team join $(team) @s
$tellraw @s {"text":"[demo] You are now on team $(team).","color":"yellow"}
