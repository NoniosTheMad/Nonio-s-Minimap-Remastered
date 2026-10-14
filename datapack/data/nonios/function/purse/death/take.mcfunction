# as the killer; #purse = the victim's coins
scoreboard players operation @s coins += #purse nx.purse
scoreboard players set @a[tag=nx.victim] coins 0
tellraw @s[type=player] [{"text":"+","color":"gold"},{"score":{"name":"#purse","objective":"nx.purse"},"color":"yellow","bold":true},{"text":" coins: you took the purse of ","color":"gold"},{"selector":"@a[tag=nx.victim]"}]
tellraw @a[tag=nx.victim] [{"selector":"@s"},{"text":" took your purse (","color":"red"},{"score":{"name":"#purse","objective":"nx.purse"},"color":"red"},{"text":" coins)","color":"red"}]
execute at @s run playsound minecraft:block.chain.break player @a ~ ~ ~ 1 0.8
