# income this match (money scale, purse/scale): every purse increase; bank withdrawals are taken back out in bank/withdraw.
# nx.plast -1 = just (re)set (match start, death, lobby): not income.
scoreboard players add @s nx.earned 0
execute if score @s nx.plast matches 0.. if score @s nx.coins > @s nx.plast run function nonios:purse/earn
# coin sound (#113): only when the purse crosses a multiple of the step, which grows with what the player gathered
execute if score @s nx.coins > @s nx.plast run function nonios:purse/pling
scoreboard players operation @s nx.plast = @s nx.coins
function nonios:purse/weight
function nonios:purse/show
