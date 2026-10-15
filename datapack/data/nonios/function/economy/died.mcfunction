# as a player who died (any cause) and respawned, from nonios:death: the killstreak ends
tag @s remove nx.k.done
execute store result score #min nx.eco run data get storage nonios:config bounty_min_streak
execute if score @s nx.streak >= #min nx.eco run tellraw @s [{"text":"Your ","color":"gray"},{"score":{"name":"@s","objective":"nx.streak"},"color":"red"},{"text":"-kill streak ended.","color":"gray"}]
scoreboard players set @s nx.streak 0
