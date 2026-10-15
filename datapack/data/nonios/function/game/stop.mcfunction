execute if score #state nx.state matches 0 run return run tellraw @s {"text":"No match running.","color":"gray"}
tellraw @a {"text":"Match stopped by an admin.","color":"red"}
function nonios:game/to_lobby
