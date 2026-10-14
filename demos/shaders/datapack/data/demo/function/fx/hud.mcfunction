# keep the current stack on the action bar while any layer is on
execute if score @s demo.look matches 1.. run return run function demo:fx/status
execute if score @s demo.col matches 1.. run return run function demo:fx/status
execute if score @s demo.line matches 1.. run return run function demo:fx/status
execute if score @s demo.dist matches 1.. run return run function demo:fx/status
