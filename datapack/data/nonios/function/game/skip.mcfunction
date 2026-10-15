execute if score #state nx.state matches 0 run return run tellraw @s {"text":"Nothing to skip.","color":"gray"}
execute if score #state nx.state matches 1 run return run function nonios:game/battle/start
execute if score #state nx.state matches 2 run return run function nonios:game/end/draw
execute if score #state nx.state matches 3 run return run function nonios:game/to_lobby
