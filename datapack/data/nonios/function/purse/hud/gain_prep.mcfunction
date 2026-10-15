# hud.g = "  +<gain>" for the popup; nx.ptime 30..1: 30-24 bright yellow bold, 23-13 gold, 12-1 dim
function nonios:purse/hud/num_store {src:"@s nx.pgain"}
data modify storage nonios:purse hn.c set value "#7A6A3A"
execute if score @s nx.ptime matches 13.. run data modify storage nonios:purse hn.c set value "gold"
execute if score @s nx.ptime matches 24.. run data modify storage nonios:purse hn.c set value "yellow"
data modify storage nonios:purse hn.b set value "false"
execute if score @s nx.ptime matches 24.. run data modify storage nonios:purse hn.b set value "true"
function nonios:purse/hud/gain with storage nonios:purse hn
