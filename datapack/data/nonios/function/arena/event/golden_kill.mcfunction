# #nonios:economy/kill_mult, as the killer: Golden Hour doubles (x golden_mult) the whole kill reward (base + bounty +
# streak/tier bonuses) when the victim died inside the Arena box. The victim's purse is never multiplied (no minting).
execute unless score #golden_t nx.arena matches 1.. run return 0
scoreboard players set #gin nx.eco 0
execute as @a[tag=nx.k.v1,limit=1] if function nonios:arena/in_bounds run scoreboard players set #gin nx.eco 1
execute unless entity @a[tag=nx.k.v1] if function nonios:arena/in_bounds run scoreboard players set #gin nx.eco 1
execute if score #gin nx.eco matches 1 run scoreboard players operation #kmul nx.eco *= #golden_mult nx.arena
