# once a second while the arena runs: Haste for a team holding a haste node, inside its own field
execute if score #haste_white nx.arena matches 1.. if data storage nonios:arena config.fields.white run function nonios:arena/bonus/haste with storage nonios:arena config.fields.white
execute if score #haste_black nx.arena matches 1.. if data storage nonios:arena config.fields.black run function nonios:arena/bonus/haste with storage nonios:arena config.fields.black
