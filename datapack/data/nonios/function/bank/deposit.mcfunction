# #bd nx.eco coins requested -> clamped to the purse; purse -> #b (team bank working copy)
scoreboard players operation #bd nx.eco < @s nx.coins
execute if score #bd nx.eco matches ..0 run return run function nonios:bank/msg {m1:"Your purse is empty.",m2:"",c:"red"}
scoreboard players operation @s nx.coins -= #bd nx.eco
scoreboard players operation #b nx.eco += #bd nx.eco
scoreboard players operation #amt nx.eco = #bd nx.eco
function nonios:bank/msg {m1:"Deposited ",m2:" coins: safe in the team bank.",c:"green"}
execute at @s run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.4
tag @s add nx.bk.me
execute if entity @s[team=white] run tellraw @a[team=white,tag=!nx.bk.me] [{"text":"🏦 ","color":"gold"},{"selector":"@s"},{"text":" deposited ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":". Team bank: ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"}]
execute if entity @s[team=black] run tellraw @a[team=black,tag=!nx.bk.me] [{"text":"🏦 ","color":"gold"},{"selector":"@s"},{"text":" deposited ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":". Team bank: ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"}]
tag @s remove nx.bk.me
