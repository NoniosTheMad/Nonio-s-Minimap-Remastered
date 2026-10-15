scoreboard players operation #drop nx.purse = @s nx.coins
scoreboard players set @s nx.coins 0
function nonios:purse/bag/spawn
tellraw @s [{"text":"You dropped your purse (","color":"red"},{"score":{"name":"#drop","objective":"nx.purse"},"color":"red"},{"text":" coins).","color":"red"}]
