# fell off the islands (y < 6): back to the last ground they stood on, floating down (feedback #79: "fell out of the world")
execute unless score @s nx.dgok matches 1 run return run function nonios:dream/void/reroll
execute store result storage nonios:dream vc.x int 1 run scoreboard players get @s nx.dgx
execute store result storage nonios:dream vc.y int 1 run scoreboard players get @s nx.dgy
execute store result storage nonios:dream vc.z int 1 run scoreboard players get @s nx.dgz
function nonios:dream/void/tp with storage nonios:dream vc
function nonios:dream/void/caught
