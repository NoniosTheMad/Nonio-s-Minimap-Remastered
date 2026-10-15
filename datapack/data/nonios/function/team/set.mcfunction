tag @s remove nx.spectator
$team join $(team) @s
$tellraw @a [{"selector":"@s"},{"text":" joined $(Team).","color":"$(color)"}]
execute at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1.5
