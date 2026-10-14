# #bw nx.eco coins requested -> clamped to the team bank; #b -> purse (carried again: slows you, lost if you are killed)
scoreboard players operation #bw nx.eco < #b nx.eco
execute if score #bw nx.eco matches ..0 run return run function nonios:bank/msg {m1:"The team bank is empty.",m2:"",c:"red"}
scoreboard players operation #b nx.eco -= #bw nx.eco
scoreboard players operation @s nx.coins += #bw nx.eco
scoreboard players operation #amt nx.eco = #bw nx.eco
function nonios:bank/msg {m1:"Withdrew ",m2:" coins into your purse.",c:"yellow"}
execute at @s run playsound minecraft:block.chain.break player @s ~ ~ ~ 1 1.2
tag @s add nx.bk.me
execute if entity @s[team=white] run tellraw @a[team=white,tag=!nx.bk.me] [{"text":"🏦 ","color":"gold"},{"selector":"@s"},{"text":" withdrew ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":". Team bank: ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"}]
execute if entity @s[team=black] run tellraw @a[team=black,tag=!nx.bk.me] [{"text":"🏦 ","color":"gold"},{"selector":"@s"},{"text":" withdrew ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":". Team bank: ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"}]
tag @s remove nx.bk.me
