# as/at a player who used a bank trigger: nx.bankt 1 open / 2 deposit all / 3 withdraw all, nx.bankd N deposit, nx.bankw N withdraw.
# Every request is re-checked here (own team's vault, prep/battle), so a dialog left open elsewhere can't move coins.
scoreboard players set #bt nx.eco 0
scoreboard players set #bd nx.eco 0
scoreboard players set #bw nx.eco 0
execute if score @s nx.bankt matches 1.. run scoreboard players operation #bt nx.eco = @s nx.bankt
execute if score @s nx.bankd matches 1.. run scoreboard players operation #bd nx.eco = @s nx.bankd
execute if score @s nx.bankw matches 1.. run scoreboard players operation #bw nx.eco = @s nx.bankw
scoreboard players reset @s nx.bankt
scoreboard players reset @s nx.bankd
scoreboard players reset @s nx.bankw
execute unless function nonios:bank/allowed run return run function nonios:bank/denied
scoreboard players add @s nx.coins 0
data remove storage nonios:bank ui.msg
execute if entity @s[team=white] run return run function nonios:bank/use {team:"white",Team:"White",color:"white"}
function nonios:bank/use {team:"black",Team:"Black",color:"light_purple"}
