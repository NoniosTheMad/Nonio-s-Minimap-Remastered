# as the victim: #purse = centre_killer_share % of it (rounded down); the rest stays in nx.coins and drops as a bag
execute store result score #share nx.purse run data get storage nonios:config centre_killer_share
scoreboard players operation #purse nx.purse *= #share nx.purse
scoreboard players set #100 nx.purse 100
scoreboard players operation #purse nx.purse /= #100 nx.purse
