$scoreboard players operation #t nx.purse = @s nx.mn.$(b)
$scoreboard players operation #t nx.purse *= #$(b) nx.coinval
$scoreboard players set @s nx.mn.$(b) 0
scoreboard players operation @s nx.mined += #t nx.purse
# debt from placing coin blocks while broke (mine/placed) is paid first
execute if score @s nx.pdebt matches 1.. run function nonios:purse/mine/repay
scoreboard players operation @s nx.coins += #t nx.purse
