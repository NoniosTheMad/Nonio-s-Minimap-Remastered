# as a killer whose streak just reached bounty_min_streak or more: everyone learns the bounty on their head
scoreboard players operation #own nx.eco = @s nx.streak
scoreboard players operation #own nx.eco *= #bper nx.eco
execute if score #bcap nx.eco matches 1.. run scoreboard players operation #own nx.eco < #bcap nx.eco
tellraw @a [{"text":"🔥 ","color":"gold"},{"selector":"@s"},{"text":" is on a ","color":"gray"},{"score":{"name":"@s","objective":"nx.streak"},"color":"red","bold":true},{"text":"-kill streak! Bounty: ","color":"gray"},{"score":{"name":"#own","objective":"nx.eco"},"color":"gold","bold":true},{"text":" coins","color":"gold"}]
execute as @a at @s run playsound minecraft:entity.blaze.shoot master @s ~ ~ ~ 0.4 1.6
