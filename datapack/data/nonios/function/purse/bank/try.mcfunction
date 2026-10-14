# as a player with coins on a bank pad (context: at the pad marker). Pads tagged nx.white / nx.black take only that team.
# An untagged pad (spike demo) banks into the player's own team.
execute if entity @n[type=marker,tag=nx.bank_zone,tag=nx.white,distance=..0.1] unless entity @s[team=white] run return run function nonios:purse/bank/wrong
execute if entity @n[type=marker,tag=nx.bank_zone,tag=nx.black,distance=..0.1] unless entity @s[team=black] run return run function nonios:purse/bank/wrong
execute if entity @s[team=white] run return run function nonios:purse/bank/deposit {team:"white"}
execute if entity @s[team=black] run return run function nonios:purse/bank/deposit {team:"black"}
function nonios:purse/bank/deposit {team:"none"}
