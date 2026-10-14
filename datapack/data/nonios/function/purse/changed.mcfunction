execute if score @s nx.coins > @s nx.plast at @s run playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.35 1.7
# income this match (money scale, purse/scale): every purse increase; bank withdrawals are taken back out in bank/withdraw.
# nx.plast -1 = just (re)set (match start, death, lobby): not income.
scoreboard players add @s nx.earned 0
execute if score @s nx.plast matches 0.. if score @s nx.coins > @s nx.plast run function nonios:purse/earn
scoreboard players operation @s nx.plast = @s nx.coins
function nonios:purse/weight
function nonios:purse/show
