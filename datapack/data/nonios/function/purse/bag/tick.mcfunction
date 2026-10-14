# as a coin bag, at it: the nearest living non-spectator player within 1.6 blocks takes it
scoreboard players operation #bag nx.purse = @s nx.coins
execute as @e[type=player,gamemode=!spectator,distance=..1.6,sort=nearest,limit=1] run function nonios:purse/bag/pickup
execute if score #bag nx.purse matches 0 run kill @s
