# as a player on their own locked pad: the unlock dialog (shows the purse; paying = /trigger nx.portal_t set 1).
# Short purse: the same dialog with "Open" greyed (no action) and a "Need N coins" tooltip (portal/offer_poor).
data modify storage nonios:portal ui set value {}
execute store result score #cost nx.portal run data get storage nonios:config dream_cost
execute store result storage nonios:portal ui.cost int 1 run scoreboard players get #cost nx.portal
scoreboard players add @s nx.coins 0
execute store result storage nonios:portal ui.coins int 1 run scoreboard players get @s nx.coins
execute if score @s nx.coins >= #cost nx.portal run return run function nonios:portal/offer_show with storage nonios:portal ui
scoreboard players operation #cost nx.portal -= @s nx.coins
execute store result storage nonios:portal ui.need int 1 run scoreboard players get #cost nx.portal
function nonios:portal/offer_poor with storage nonios:portal ui
