# per match (game/reset_world) and on map/build: nothing paid yet, altars redrawn for the current team levels
scoreboard players set #white_iron nx.altar 0
scoreboard players set #white_gold nx.altar 0
scoreboard players set #white_diamond nx.altar 0
scoreboard players set #black_iron nx.altar 0
scoreboard players set #black_gold nx.altar 0
scoreboard players set #black_diamond nx.altar 0
function nonios:altar/refresh {team:"white"}
function nonios:altar/refresh {team:"black"}
