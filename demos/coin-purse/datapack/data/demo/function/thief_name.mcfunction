scoreboard players operation @s demo.c = @s nx.coins
execute store result storage demo:state thief.n int 1 run scoreboard players get @s nx.coins
function demo:thief_name2 with storage demo:state thief
