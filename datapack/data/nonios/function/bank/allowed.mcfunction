# succeeds when @s may use their team bank here. #why nx.eco = reason on failure:
# 1 no match in prep/battle, 2 not on a team, 3 at the other team's vault, 4 not near their own vault
scoreboard players set #why nx.eco 1
execute unless score #state nx.state matches 1..2 run return fail
scoreboard players set #why nx.eco 2
execute unless entity @s[team=white] unless entity @s[team=black] run return fail
scoreboard players set #why nx.eco 4
execute if function nonios:bank/near run return 1
return fail
