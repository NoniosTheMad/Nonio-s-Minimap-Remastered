# as a Dream animal seen for the first time: its loot (emeralds; 1 in 100/#gleam_pct gleams and drops far more)
tag @s add nx.dfauna
execute if predicate nonios:dream/baby run return run data modify entity @s DeathLootTable set value "nonios:dream/none"
execute store result score #r nx.dream run random value 1..100
execute if score #r nx.dream <= #gleam_pct nx.dream run return run function nonios:dream/fauna/gleam
data modify entity @s DeathLootTable set value "nonios:dream/fauna"
