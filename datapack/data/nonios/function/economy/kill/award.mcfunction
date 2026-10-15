# as the killer. In: #vs nx.eco = victim's streak, #bonus nx.eco = hook bonus, victim = @a[tag=nx.k.v1] (else storage nonios:eco vname)
execute store result score #base nx.eco run data get storage nonios:config kill_reward
execute store result score #bper nx.eco run data get storage nonios:config bounty_per_kill
execute store result score #min nx.eco run data get storage nonios:config bounty_min_streak
execute store result score #bcap nx.eco run data get storage nonios:config bounty_cap
# bounty for ending the victim's streak
scoreboard players set #bty nx.eco 0
execute if score #vs nx.eco >= #min nx.eco run scoreboard players operation #bty nx.eco = #vs nx.eco
scoreboard players operation #bty nx.eco *= #bper nx.eco
execute if score #bcap nx.eco matches 1.. run scoreboard players operation #bty nx.eco < #bcap nx.eco
scoreboard players operation #sum nx.eco = #base nx.eco
scoreboard players operation #sum nx.eco += #bty nx.eco
scoreboard players operation #sum nx.eco += #bonus nx.eco
scoreboard players operation @s nx.coins += #sum nx.eco
scoreboard players operation @s nx.krw += #base nx.eco
scoreboard players operation @s nx.kbty += #bty nx.eco
scoreboard players operation @s nx.kbon += #bonus nx.eco
tag @s add nx.k.show
execute at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.6
# announcements
execute if score #bty nx.eco matches 1.. if entity @a[tag=nx.k.v1] run tellraw @a [{"text":"☠ ","color":"red"},{"selector":"@s"},{"text":" ended ","color":"gray"},{"selector":"@a[tag=nx.k.v1]"},{"text":"'s ","color":"gray"},{"score":{"name":"#vs","objective":"nx.eco"},"color":"red"},{"text":"-kill streak: +","color":"gray"},{"score":{"name":"#bty","objective":"nx.eco"},"color":"gold","bold":true},{"text":" bounty","color":"gold"}]
execute if score #bty nx.eco matches 1.. unless entity @a[tag=nx.k.v1] run tellraw @a [{"text":"☠ ","color":"red"},{"selector":"@s"},{"text":" ended ","color":"gray"},{"nbt":"vname","storage":"nonios:eco","color":"white"},{"text":"'s ","color":"gray"},{"score":{"name":"#vs","objective":"nx.eco"},"color":"red"},{"text":"-kill streak: +","color":"gray"},{"score":{"name":"#bty","objective":"nx.eco"},"color":"gold","bold":true},{"text":" bounty","color":"gold"}]
scoreboard players add @s nx.streak 1
execute if score @s nx.streak >= #min nx.eco run function nonios:economy/kill/streak_msg
