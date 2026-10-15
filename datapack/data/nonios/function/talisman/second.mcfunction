# once a second in prep and battle (game/prep/second, game/battle/second): pay everyone wearing a talisman
scoreboard players operation #t nx.talis += #speed nx.talis
execute store result score #p nx.talis run data get storage nonios:config talisman_period
execute if score #t nx.talis < #p nx.talis run return 0
scoreboard players set #t nx.talis 0
execute store result score #c nx.talis run data get storage nonios:config talisman_coins
execute as @a[gamemode=!spectator] if items entity @s armor.head *[minecraft:custom_data~{nx_talisman:1b}] run scoreboard players operation @s nx.coins += #c nx.talis
