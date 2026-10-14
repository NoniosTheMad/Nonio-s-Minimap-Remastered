scoreboard players operation @s demo.c = @s coins
execute store result storage demo:state thief.n int 1 run scoreboard players get @s coins
function demo:thief_name2 with storage demo:state thief
