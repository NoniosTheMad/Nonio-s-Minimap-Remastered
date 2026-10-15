# {b}: as a player who mined N blocks of b (stat nx.mn.<b>). Yield in hundredths = N * #<b> nx.coinval * (100 + Fortune
# level of the held tool * #fortune_pct) / 100. Whole coins go to the purse (debt first), the rest stays in nx.pfrac.
$scoreboard players operation #t nx.purse = @s nx.mn.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
$scoreboard players set @s nx.mn.$(b) 0
function nonios:purse/mine/fortune
scoreboard players operation #f nx.purse *= #fortune_pct nx.coinval
scoreboard players add #f nx.purse 100
scoreboard players operation #t nx.purse *= #f nx.purse
scoreboard players operation #t nx.purse /= #100 nx.purse
scoreboard players add @s nx.pfrac 0
scoreboard players operation @s nx.pfrac += #t nx.purse
scoreboard players operation #t nx.purse = @s nx.pfrac
scoreboard players operation #t nx.purse /= #100 nx.purse
scoreboard players operation @s nx.pfrac %= #100 nx.purse
execute if score #t nx.purse matches ..0 run return 0
scoreboard players operation @s nx.mined += #t nx.purse
# debt from placing coin blocks while broke (mine/placed) is paid first
execute if score @s nx.pdebt matches 1.. run function nonios:purse/mine/repay
scoreboard players operation @s nx.coins += #t nx.purse
