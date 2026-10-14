# #nonios:economy/kill_bonus entry (as the dead victim): Bounty Hunt running and the victim died inside the Arena
execute unless score #bounty_t nx.arena matches 1.. run return 0
execute at @s run function nonios:arena/event/bounty_in with storage nonios:arena config.bounds
