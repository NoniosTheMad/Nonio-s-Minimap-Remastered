# as the victim (dead): team-kill check, their streak -> bounty, bonus hook. Tag nx.k.done = already paid out (cleared on respawn).
tag @s add nx.k.done
execute if entity @s[team=white] if entity @a[tag=nx.k.killer,team=white] run scoreboard players set #tk nx.eco 1
execute if entity @s[team=black] if entity @a[tag=nx.k.killer,team=black] run scoreboard players set #tk nx.eco 1
scoreboard players add @s nx.streak 0
scoreboard players operation #vs nx.eco = @s nx.streak
# Bonus hook for classes/tiers: functions in #nonios:economy/kill_bonus run as the victim (killer = @a[tag=nx.k.killer])
# and add their bonus to #bonus nx.eco.
function #nonios:economy/kill_bonus
data modify storage nonios:eco vname set value ""
