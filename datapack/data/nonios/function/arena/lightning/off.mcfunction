scoreboard players set #lt_set nx.arena 0
scoreboard players set #lt_on nx.arena 0
function nonios:arena/lightning/despawn
tellraw @a [{text:"⚡ ",color:"gray"},{text:"Lightning OFF",color:"gray",bold:true}]
