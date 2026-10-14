# as a player who used /trigger nx.team: 1 open picker, 2 White, 3 Black, 4 auto (smaller team), 5 no team (spectate)
scoreboard players operation #tv nx.tmp = @s nx.team
scoreboard players reset @s nx.team
execute if score #tv nx.tmp matches 1 run function nonios:team/open
execute if score #tv nx.tmp matches 2 run function nonios:team/pick {team:"white",Team:"White",color:"white"}
execute if score #tv nx.tmp matches 3 run function nonios:team/pick {team:"black",Team:"Black",color:"light_purple"}
execute if score #tv nx.tmp matches 4 run function nonios:team/auto_pick
execute if score #tv nx.tmp matches 5 run function nonios:team/leave
