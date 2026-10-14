# test/demo only: switch @s to $(team) even mid-match (keeps gear and coins; teleports to that base when a match runs)
$team join $(team) @s
tag @s remove nx.spectator
$tellraw @s {"text":"You are now on $(Team).","color":"$(color)"}
$execute if score #state nx.state matches 1..2 run function nonios:game/enter {team:"$(team)"}
