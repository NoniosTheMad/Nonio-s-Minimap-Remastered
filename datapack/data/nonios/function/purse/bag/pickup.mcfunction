scoreboard players operation @s nx.coins += #bag nx.purse
tellraw @s [{"text":"+","color":"gold"},{"score":{"name":"#bag","objective":"nx.purse"},"color":"yellow","bold":true},{"text":" coins (picked up a purse)","color":"gold"}]
execute at @s run playsound minecraft:block.chain.break player @a ~ ~ ~ 1 1.3
scoreboard players set #bag nx.purse 0
