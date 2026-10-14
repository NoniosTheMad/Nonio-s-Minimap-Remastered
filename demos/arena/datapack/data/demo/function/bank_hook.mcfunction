# Demo handler for #nonios:arena/on_node_payout (as + at the node). Bank mode: credit the team's bank and
# set #handled so the default loot drop is skipped. A real team bank does the same.
execute unless score #bank demo.c matches 1 run return 0
execute store result score #c demo.c run data get storage nonios:arena payout.coins
execute if data storage nonios:arena payout{team:"white"} run scoreboard players operation White demo.bank += #c demo.c
execute if data storage nonios:arena payout{team:"black"} run scoreboard players operation Black demo.bank += #c demo.c
scoreboard players set #handled nx.arena 1
tellraw @a [{text:"[bank] +",color:"gold"},{storage:"nonios:arena",nbt:"payout.coins",color:"yellow"},{text:" coins to ",color:"gold"},{storage:"nonios:arena",nbt:"payout.team"},{text:" from the ",color:"gold"},{storage:"nonios:arena",nbt:"payout.name",color:"yellow"}]
