scoreboard players operation #drop nx.purse = @s coins
scoreboard players set @s coins 0
function nonios:purse/bag/spawn
tellraw @s [{"text":"You dropped your purse (","color":"red"},{"score":{"name":"#drop","objective":"nx.purse"},"color":"red"},{"text":" coins) where you died. Anyone can grab it for 5 min.","color":"red"}]
