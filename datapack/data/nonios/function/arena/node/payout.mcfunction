# as + at a held node marker whose payout timer ran out
scoreboard players operation @s nx.ar_t += @s nx.ar_iv
execute if score @s nx.ar_t matches ..0 run scoreboard players operation @s nx.ar_t = @s nx.ar_iv
data modify storage nonios:arena payout set value {team:"white",loot:""}
execute if score @s nx.ar_own matches 2 run data modify storage nonios:arena payout.team set value "black"
data modify storage nonios:arena payout.node set from entity @s data.id
data modify storage nonios:arena payout.name set from entity @s data.name
data modify storage nonios:arena payout.loot set from entity @s data.loot
# rolls = (1 + (holding team size - 1) / per_roll) x #mult; coins = node coins x #mult
execute if score @s nx.ar_own matches 1 store result score #n nx.arena if entity @a[team=white]
execute if score @s nx.ar_own matches 2 store result score #n nx.arena if entity @a[team=black]
execute if score #sim nx.arena matches 1.. run scoreboard players operation #n nx.arena = #sim nx.arena
scoreboard players remove #n nx.arena 1
execute if score #n nx.arena matches ..-1 run scoreboard players set #n nx.arena 0
scoreboard players operation #n nx.arena /= #per_roll nx.arena
scoreboard players add #n nx.arena 1
scoreboard players operation #n nx.arena *= #mult nx.arena
execute store result storage nonios:arena payout.rolls int 1 run scoreboard players get #n nx.arena
execute store result score #c nx.arena run data get entity @s data.coins
scoreboard players operation #c nx.arena *= #mult nx.arena
execute store result storage nonios:arena payout.coins int 1 run scoreboard players get #c nx.arena
# hook first; then the node's bonus; loot only for nodes that have one
scoreboard players set #handled nx.arena 0
function #nonios:arena/on_node_payout
execute if data entity @s data{bonus:"interest"} run function nonios:arena/bonus/interest with storage nonios:arena payout
execute if score #handled nx.arena matches 0 unless data storage nonios:arena payout{loot:""} run function nonios:arena/node/drop
scoreboard players add #payouts nx.arena 1
