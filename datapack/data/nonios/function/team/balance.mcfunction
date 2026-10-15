# match start: teamless players (not opted out with "No team") join the smaller team;
# with auto_balance, then move random players from the bigger team until the gap is <= 1
execute as @a[team=,tag=!nx.spectator] run function nonios:team/auto_pick
execute if data storage nonios:config {auto_balance:1b} run function nonios:team/even
