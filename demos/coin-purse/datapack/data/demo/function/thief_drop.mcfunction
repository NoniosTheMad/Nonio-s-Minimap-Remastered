# the thief died holding a purse: it drops as a coin bag (same bag as a player death without a player killer)
scoreboard players operation #drop nx.purse = #thief demo.c
scoreboard players set #thief demo.c 0
function nonios:purse/bag/spawn
tellraw @a [{"text":"[demo] The Purse Thief dropped ","color":"yellow"},{"score":{"name":"#drop","objective":"nx.purse"},"color":"gold"},{"text":" coins. Walk over the bag.","color":"yellow"}]
