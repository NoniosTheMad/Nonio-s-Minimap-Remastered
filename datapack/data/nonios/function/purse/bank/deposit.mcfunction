# STUB bank: moves the whole purse into nx.bank (safe, weightless). No withdraw yet.
scoreboard players operation @s nx.bank += @s coins
tellraw @s [{"text":"Deposited ","color":"green"},{"score":{"name":"@s","objective":"coins"},"color":"yellow","bold":true},{"text":" coins. Bank: ","color":"green"},{"score":{"name":"@s","objective":"nx.bank"},"color":"yellow"}]
execute at @s run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.4
scoreboard players set @s coins 0
