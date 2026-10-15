# as the killer; #purse = the victim's coins (or the killer's share of them, death/split). What is left drops (death/died).
execute unless score #purse nx.purse matches 1.. run return 0
scoreboard players operation @s nx.coins += #purse nx.purse
scoreboard players operation @a[tag=nx.victim] nx.coins -= #purse nx.purse
# kill actionbar (economy/kill/show, next tick): the purse taken is listed next to the kill reward
scoreboard players operation @s[type=player] nx.kpurse += #purse nx.purse
tag @s[type=player] add nx.k.show
tellraw @s[type=player] [{"text":"+","color":"gold"},{"score":{"name":"#purse","objective":"nx.purse"},"color":"yellow","bold":true},{"text":" coins: you took the purse of ","color":"gold"},{"selector":"@a[tag=nx.victim]"}]
tellraw @a[tag=nx.victim] [{"selector":"@s"},{"text":" took your purse (","color":"red"},{"score":{"name":"#purse","objective":"nx.purse"},"color":"red"},{"text":" coins)","color":"red"}]
execute at @s run playsound minecraft:block.chain.break player @a ~ ~ ~ 1 0.8
