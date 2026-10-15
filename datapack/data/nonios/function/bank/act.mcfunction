# as/at a player who used a bank trigger: nx.bankt 1 open / 3 withdraw all / 4 withdraw half, nx.bankw N withdraw N.
# Every request is re-checked here (own team's vault, prep/battle), so a dialog left open elsewhere can't move coins.
scoreboard players set #bt nx.eco 0
scoreboard players set #bw nx.eco 0
execute if score @s nx.bankt matches 1.. run scoreboard players operation #bt nx.eco = @s nx.bankt
execute if score @s nx.bankw matches 1.. run scoreboard players operation #bw nx.eco = @s nx.bankw
scoreboard players reset @s nx.bankt
scoreboard players reset @s nx.bankw
execute unless function nonios:bank/allowed run return run function nonios:bank/denied
scoreboard players add @s nx.coins 0
execute if entity @s[team=white] run return run function nonios:bank/use {team:"white",Team:"White",color:"white"}
function nonios:bank/use {team:"black",Team:"Black",color:"light_purple"}
