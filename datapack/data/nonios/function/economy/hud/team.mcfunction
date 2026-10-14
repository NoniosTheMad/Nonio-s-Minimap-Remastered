# {team}: values for that team's sidebar (economy/rate and #nx nx.eco already computed) -> hud/set
$data modify storage nonios:eco hud set value {team:"$(team)",cap:""}
$execute store result storage nonios:eco hud.b int 1 run scoreboard players get #$(team) nx.bank
execute store result storage nonios:eco hud.rw int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:eco hud.rt int 1 run scoreboard players get #rt nx.eco
$execute store result storage nonios:eco hud.l int 1 run scoreboard players get #last_$(team) nx.eco
execute store result storage nonios:eco hud.n int 1 run scoreboard players get #nx nx.eco
$execute if score #capped_$(team) nx.eco matches 1 run data modify storage nonios:eco hud.cap set value " max"
function nonios:economy/hud/set with storage nonios:eco hud
