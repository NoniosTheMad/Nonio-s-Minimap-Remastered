# as + at a held node marker whose payout timer ran out: the hook, then the node's bonus (#127: nodes never drop items)
scoreboard players operation @s nx.ar_t += @s nx.ar_iv
execute if score @s nx.ar_t matches ..0 run scoreboard players operation @s nx.ar_t = @s nx.ar_iv
data modify storage nonios:arena payout set value {team:"white"}
execute if score @s nx.ar_own matches 2 run data modify storage nonios:arena payout.team set value "black"
data modify storage nonios:arena payout.node set from entity @s data.id
data modify storage nonios:arena payout.name set from entity @s data.label
data modify storage nonios:arena payout.bonus set from entity @s data.bonus
function #nonios:arena/on_node_payout
execute if data entity @s data{bonus:"interest"} run function nonios:arena/bonus/interest with storage nonios:arena payout
scoreboard players add #payouts nx.arena 1
