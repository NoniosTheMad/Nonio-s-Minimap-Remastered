# toggle: simulated team size 20 <-> real (-1 = off)
execute if score #sim nx.gen matches 1.. run scoreboard players set #sim nx.gen -1
execute if score #sim nx.gen matches -1 run return run function demo:say {m:"Team size: real players again (1 roll per drop for 1-4 players)"}
scoreboard players set #sim nx.gen 20
function demo:say {m:"Simulating 20 players per team: 5 rolls per drop (1 + 19/4)"}
