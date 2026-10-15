# {team}: values for that team's sidebar (economy/rate already computed) -> hud/set
$data modify storage nonios:eco hud set value {team:"$(team)",cap:""}
$execute store result storage nonios:eco hud.b int 1 run scoreboard players get #$(team) nx.bank
data modify storage nonios:eco hud.r set from storage nonios:eco rtxt
data modify storage nonios:eco hud.u set from storage nonios:eco unit
$execute store result storage nonios:eco hud.l int 1 run scoreboard players get #last_$(team) nx.eco
$execute if score #capped_$(team) nx.eco matches 1 run data modify storage nonios:eco hud.cap set value " max"
function nonios:economy/hud/set with storage nonios:eco hud
