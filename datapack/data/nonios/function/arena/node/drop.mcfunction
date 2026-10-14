# as + at a node marker: default payout = loot at the node (held while item_cap stacks lie around)
execute store result score #items nx.arena if entity @e[type=item,distance=..3]
execute if score #items nx.arena >= #item_cap nx.arena run return run scoreboard players add #held nx.arena 1
execute store result score #left nx.arena run data get storage nonios:arena payout.rolls
function nonios:arena/node/drop_roll with storage nonios:arena payout
particle minecraft:happy_villager ~ ~1 ~ 0.6 0.4 0.6 0 12
playsound minecraft:entity.experience_orb.pickup block @a ~ ~ ~ 1.5 0.8
