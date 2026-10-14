# every second (purse/tick): the money scale S (percent) per team, then each player's weight at their team's S.
#   S = min(max(100 + w_grow * match minutes, 100 + team average nx.earned * 100 / w_iref), w_smax)
# Match minutes count from the match start (#t0 nx.eco, economy/match_start); outside a match S = 100.
scoreboard players set #st nx.purse 100
execute if score #state nx.state matches 1..2 run function nonios:purse/scale_time
function nonios:purse/scale_team {team:"white"}
function nonios:purse/scale_team {team:"black"}
execute as @a[team=white] unless score @s nx.pscale = #s_white nx.purse run function nonios:purse/rescale {team:"white"}
execute as @a[team=black] unless score @s nx.pscale = #s_black nx.purse run function nonios:purse/rescale {team:"black"}
execute as @a[team=] unless score @s nx.pscale matches 100 run function nonios:purse/rescale {team:"none"}
