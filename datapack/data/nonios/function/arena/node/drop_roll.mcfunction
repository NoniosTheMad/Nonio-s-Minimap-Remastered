$loot spawn ~ ~1 ~ loot $(loot)
scoreboard players remove #left nx.arena 1
execute if score #left nx.arena matches 1.. run function nonios:arena/node/drop_roll with storage nonios:arena payout
