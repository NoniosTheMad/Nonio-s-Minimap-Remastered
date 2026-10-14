$team join $(team) @s
$tellraw @a [{"text":"Auto-balance: ","color":"gray"},{"selector":"@s"},{"text":" moved to $(Team).","color":"$(color)"}]
function nonios:team/even
