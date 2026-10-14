# as a player on their own locked pad: the unlock dialog (shows the purse; paying = /trigger nx.portal_t set 1)
data modify storage nonios:portal ui set value {}
execute store result storage nonios:portal ui.cost int 1 run data get storage nonios:config dream_cost
execute store result storage nonios:portal ui.coins int 1 run scoreboard players get @s nx.coins
function nonios:portal/offer_show with storage nonios:portal ui
