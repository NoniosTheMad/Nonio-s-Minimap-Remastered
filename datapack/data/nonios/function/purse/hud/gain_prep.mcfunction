# hud.g = "  +<gain>" for the popup; first 6 ticks bright yellow bold, last 12 dim, gold between (#114)
function nonios:purse/hud/num_store {src:"@s nx.pgain"}
data modify storage nonios:purse hn.c set value "#7A6A3A"
execute if score @s nx.ptime matches 13.. run data modify storage nonios:purse hn.c set value "gold"
execute if score @s nx.page matches ..6 run data modify storage nonios:purse hn.c set value "yellow"
data modify storage nonios:purse hn.b set value "false"
execute if score @s nx.page matches ..6 run data modify storage nonios:purse hn.b set value "true"
function nonios:purse/hud/gain with storage nonios:purse hn
