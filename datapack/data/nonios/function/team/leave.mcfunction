execute if score #state nx.state matches 1..2 unless entity @s[team=] run return run tellraw @s {"text":"You can't leave your team during a match.","color":"red"}
team leave @s
tag @s add nx.spectator
tellraw @s {"text":"No team: you will watch the next match as a spectator.","color":"gray"}
